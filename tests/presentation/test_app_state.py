import pytest
from unittest.mock import MagicMock
from desktop_client.presentation.state.app_state import AppState
from desktop_client.presentation.state.config_state import ConfigState

def test_app_state_config_state_spam_protection():
    # Arrange
    app_state = AppState()
    mock_spy = MagicMock()
    app_state.config_state_changed.connect(mock_spy)
    
    # Act
    # Трижды подряд присвоить app_state.config_state = ConfigState.READY
    app_state.config_state = ConfigState.READY
    app_state.config_state = ConfigState.READY
    app_state.config_state = ConfigState.READY
    
    # Assert
    # Шпион должен зафиксировать только один вызов
    assert app_state.config_state == ConfigState.READY
    mock_spy.assert_called_once_with(ConfigState.READY)
