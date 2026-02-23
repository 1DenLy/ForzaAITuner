import pytest
from unittest.mock import MagicMock
from PySide6.QtCore import Qt

from desktop_client.presentation.views.main_window import MainWindow
from desktop_client.presentation.state.session_state import SessionState
from desktop_client.presentation.state.app_state import AppState

@pytest.fixture
def mock_vm():
    vm = MagicMock()
    vm.app_state = AppState()
    return vm

@pytest.fixture
def mock_dialog_service():
    return MagicMock()

def test_main_window_hardware_lock(qtbot, mock_vm, mock_dialog_service):
    # Arrange
    window = MainWindow(mock_vm, mock_dialog_service)
    qtbot.addWidget(window)
    
    # Act
    # Изменить замоканный стейт
    mock_vm.app_state.session_state = SessionState.RECORDING
    window._update_session_ui(SessionState.RECORDING)
    
    # Assert
    # Свойство btn_config.isEnabled() должно быть False
    assert window.btn_config.isEnabled() is False
    
    # С помощью qtbot.mouseClick() кликнуть по кнопке "Config"
    qtbot.mouseClick(window.btn_config, Qt.LeftButton)
    
    # Мок-сервис диалогов не должен быть вызван
    mock_dialog_service.show_config_dialog.assert_not_called()

def test_main_window_shutdown_on_close(qtbot, mock_vm, mock_dialog_service):
    # Arrange
    window = MainWindow(mock_vm, mock_dialog_service)
    qtbot.addWidget(window)
    mock_event = MagicMock()
    
    # Act
    window.closeEvent(mock_event)
    
    # Assert
    # Метод _vm.shutdown() должен быть вызван ровно 1 раз
    mock_vm.shutdown.assert_called_once()
    mock_event.accept.assert_called_once()

def test_main_window_buttons_normal_state_calls_dialog_service(qtbot, mock_vm, mock_dialog_service):
    # Arrange
    window = MainWindow(mock_vm, mock_dialog_service)
    qtbot.addWidget(window)
    # Set to a normal state
    mock_vm.app_state.session_state = SessionState.IDLE
    window._update_session_ui(SessionState.IDLE)
    
    # Act
    qtbot.mouseClick(window.btn_config, Qt.LeftButton)
    qtbot.mouseClick(window.btn_settings, Qt.LeftButton)
    
    # Assert
    mock_dialog_service.show_config_dialog.assert_called_once()
    mock_dialog_service.show_settings_dialog.assert_called_once()
