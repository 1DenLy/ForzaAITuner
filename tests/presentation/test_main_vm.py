import pytest
from unittest.mock import MagicMock
from src.presentation.viewmodels.main_vm import MainViewModel
from src.presentation.state.app_state import ApplicationState
from src.presentation.interfaces.protocols import ICoreFacade, IConfigValidator

@pytest.fixture
def mock_facade():
    return MagicMock(spec=ICoreFacade)

@pytest.fixture
def mock_validator():
    return MagicMock(spec=IConfigValidator)

@pytest.fixture
def viewModel(mock_facade, mock_validator):
    return MainViewModel(mock_facade, mock_validator)

def test_initial_state_is_idle(viewModel):
    assert viewModel.state == ApplicationState.IDLE

def test_load_config_valid_sets_ready(viewModel, mock_validator):
    mock_validator.validate.return_value = [] # No errors
    
    viewModel.load_config("valid.json")
    
    assert viewModel.state == ApplicationState.READY
    mock_validator.validate.assert_called_once_with("valid.json")

def test_load_invalid_config_sets_error_state(viewModel, mock_validator):
    mock_validator.validate.return_value = ["Invalid JSON", "Missing Field"]
    
    # We can also spy on the signal if we want to be thorough, 
    # but checking state is primary here.
    viewModel.load_config("invalid.json")
    
    assert viewModel.state == ApplicationState.ERROR
    mock_validator.validate.assert_called_once_with("invalid.json")

def test_start_session_calls_facade(viewModel, mock_facade, mock_validator):
    # Setup READY state
    mock_validator.validate.return_value = []
    viewModel.load_config("config.json")
    
    viewModel.toggle_session()
    
    assert viewModel.state == ApplicationState.RACING
    mock_facade.start_tracking.assert_called_once()

def test_stop_session_calls_facade(viewModel, mock_facade, mock_validator):
    # Setup RACING state
    mock_validator.validate.return_value = []
    viewModel.load_config("config.json")
    viewModel.toggle_session() # To RACING
    
    viewModel.toggle_session() # To STOP
    
    # It momentarily goes to SAVING then READY in our synchronous stub
    assert viewModel.state == ApplicationState.READY
    mock_facade.stop_tracking.assert_called_once()

def test_shutdown_cleanup_calls_facade(viewModel, mock_facade):
    viewModel.shutdown()
    mock_facade.cleanup.assert_called_once()
