import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from desktop_client.presentation.viewmodels.main_vm import MainViewModel
from desktop_client.presentation.state.config_state import ConfigState
from desktop_client.presentation.state.session_state import SessionState
from desktop_client.presentation.interfaces.protocols import ITelemetryManager


@pytest.fixture
def mock_telemetry_manager():
    tm = MagicMock(spec=ITelemetryManager)
    tm.start_session = AsyncMock()
    tm.stop_session = AsyncMock()
    return tm


@pytest.fixture
def viewModel(mock_telemetry_manager):
    vm = MainViewModel(mock_telemetry_manager)
    yield vm


def test_initial_state_is_idle(viewModel):
    assert viewModel.app_state.session_state == SessionState.IDLE
    assert viewModel.app_state.config_state == ConfigState.EMPTY


@pytest.mark.asyncio
async def test_start_recording_sets_recording_state(viewModel):
    """Config gate is bypassed by manually setting READY state."""
    viewModel.app_state.config_state = ConfigState.READY

    await viewModel.start_recording()

    assert viewModel.app_state.session_state == SessionState.RECORDING
    viewModel._telemetry_manager.start_session.assert_called_once()


@pytest.mark.asyncio
async def test_stop_session_calls_tm(viewModel):
    viewModel.app_state.config_state = ConfigState.READY
    await viewModel.start_recording()  # → RECORDING

    await viewModel.stop_recording()  # → IDLE

    assert viewModel.app_state.session_state == SessionState.IDLE
    viewModel._telemetry_manager.stop_session.assert_called_once()


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
