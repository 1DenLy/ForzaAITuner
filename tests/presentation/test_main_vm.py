import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from desktop_client.presentation.viewmodels.main_vm import MainViewModel
from desktop_client.presentation.state.config_state import ConfigState
from desktop_client.presentation.state.session_state import SessionState
from desktop_client.presentation.interfaces.protocols import IConfigValidator, IConfigRepository, ITelemetryManager

@pytest.fixture
def mock_validator():
    return MagicMock(spec=IConfigValidator)

@pytest.fixture
def mock_repo():
    return MagicMock(spec=IConfigRepository)

@pytest.fixture
def mock_telemetry_manager():
    tm = MagicMock(spec=ITelemetryManager)
    tm.start_session = AsyncMock()
    tm.stop_session = AsyncMock()
    return tm

@pytest.fixture
def viewModel(mock_validator, mock_repo, mock_telemetry_manager):
    # Inject dependencies
    vm = MainViewModel(mock_validator, mock_repo, mock_telemetry_manager)
    yield vm

def test_initial_state_is_idle(viewModel):
    assert viewModel.app_state.session_state == SessionState.IDLE
    assert viewModel.app_state.config_state == ConfigState.EMPTY

def test_load_config_valid_sets_ready(viewModel, mock_validator):
    mock_validator.validate.return_value = [] # No errors
    
    viewModel.load_config("valid.json")
    
    assert viewModel.app_state.config_state == ConfigState.READY
    mock_validator.validate.assert_called_once_with("valid.json")

def test_load_invalid_config_sets_error_state(viewModel, mock_validator):
    mock_validator.validate.return_value = ["Invalid JSON", "Missing Field"]
    
    viewModel.load_config("invalid.json")
    
    assert viewModel.app_state.config_state == ConfigState.INVALID
    mock_validator.validate.assert_called_once_with("invalid.json")

@pytest.mark.asyncio
async def test_start_session_calls_tm(viewModel, mock_validator):
    # Setup READY state
    mock_validator.validate.return_value = []
    viewModel.load_config("config.json")
    
    # We call start_recording directly to test async behavior
    await viewModel.start_recording()
    
    assert viewModel.app_state.session_state == SessionState.RECORDING
    viewModel._telemetry_manager.start_session.assert_called_once()

@pytest.mark.asyncio
async def test_stop_session_calls_tm(viewModel, mock_validator):
    # Setup RACING state
    mock_validator.validate.return_value = []
    viewModel.load_config("config.json")
    await viewModel.start_recording() # To RECORDING
    
    await viewModel.stop_recording() # To STOP/IDLE
    
    assert viewModel.app_state.session_state == SessionState.IDLE
    viewModel._telemetry_manager.stop_session.assert_called_once()

def test_load_config_during_recording_emits_error(viewModel, mock_validator):
    viewModel.app_state.session_state = SessionState.RECORDING
    
    mock_emit = MagicMock()
    viewModel.error_occurred.connect(mock_emit)
    
    viewModel.load_config("test.json")
    
    mock_validator.validate.assert_not_called()
    mock_emit.assert_called_once_with("Cannot load config while session is active.")

@pytest.mark.asyncio
async def test_start_recording_network_error_resets_state_and_emits_error(viewModel, mock_telemetry_manager):
    mock_telemetry_manager.start_session.side_effect = ConnectionError("UDP bind failed")
    
    mock_emit = MagicMock()
    viewModel.error_occurred.connect(mock_emit)
    
    await viewModel.start_recording()
    
    assert viewModel.app_state.session_state == SessionState.IDLE
    mock_emit.assert_called_once()
    assert "UDP bind failed" in mock_emit.call_args[0][0]

@pytest.mark.asyncio
async def test_start_recording_unexpected_error_resets_state_and_raises(viewModel, mock_telemetry_manager):
    mock_telemetry_manager.start_session.side_effect = TypeError("NoneType is not iterable")
    
    with pytest.raises(TypeError, match="NoneType is not iterable"):
        await viewModel.start_recording()
        
    assert viewModel.app_state.session_state == SessionState.IDLE

def test_validate_and_apply_config_io_error_sets_invalid_and_emits(viewModel, mock_repo):
    mock_repo.save_config.side_effect = IOError("Permission denied")
    
    mock_emit = MagicMock()
    viewModel.error_occurred.connect(mock_emit)
    
    viewModel.validate_and_apply_config({"key": "value"})
    
    assert viewModel.app_state.config_state == ConfigState.INVALID
    mock_emit.assert_called_once_with("Failed to apply config: Permission denied")

def test_load_last_config_success(viewModel, mock_repo, mock_validator):
    mock_repo.get_last_config_path.return_value = "last_config.json"
    mock_validator.validate.return_value = []
    
    with patch("os.path.exists", return_value=True):
        viewModel.load_last_config()
        
    assert viewModel.app_state.config_state == ConfigState.READY
    mock_validator.validate.assert_called_once_with("last_config.json")

def test_load_last_config_file_not_found(viewModel, mock_repo):
    mock_repo.get_last_config_path.return_value = "last_config.json"
    
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="Last configuration not found"):
            viewModel.load_last_config()

def test_toggle_session_starts_recording(viewModel):
    viewModel.app_state.session_state = SessionState.IDLE
    viewModel.app_state.config_state = ConfigState.READY
    
    with patch("asyncio.get_event_loop") as mock_loop:
        mock_loop.return_value.create_task = MagicMock()
        with patch.object(viewModel, 'start_recording', new=MagicMock(return_value="dummy_coro")):
            viewModel.toggle_session()
            mock_loop.return_value.create_task.assert_called_once_with("dummy_coro")

def test_toggle_session_stops_recording(viewModel):
    viewModel.app_state.session_state = SessionState.RECORDING
    
    with patch("asyncio.get_event_loop") as mock_loop:
        mock_loop.return_value.create_task = MagicMock()
        with patch.object(viewModel, 'stop_recording', new=MagicMock(return_value="dummy_coro")):
            viewModel.toggle_session()
            mock_loop.return_value.create_task.assert_called_once_with("dummy_coro")

def test_validate_and_apply_config_success(viewModel, mock_repo, mock_validator):
    config_data = {"some": "data"}
    mock_repo.save_config.return_value = "new_config.json"
    mock_validator.validate.return_value = []
    
    viewModel.validate_and_apply_config(config_data)
    
    mock_repo.save_config.assert_called_once_with(config_data)
    assert viewModel.app_state.config_state == ConfigState.READY
