import pytest
from unittest.mock import MagicMock
from PySide6.QtWidgets import QDialogButtonBox, QMessageBox, QFileDialog
from PySide6.QtCore import Qt

from desktop_client.presentation.views.config_dialog import ConfigDialog
from desktop_client.presentation.viewmodels.config_viewmodel import ConfigViewModel

@pytest.fixture
def view_model_mock():
    # Make sure we use an actual QObject for signals to work
    vm = ConfigViewModel(MagicMock(), MagicMock())
    return vm

@pytest.fixture
def config_dialog(view_model_mock, qtbot, monkeypatch):
    # Mock mapper to avoid complex UI setup requirement if any
    dialog = ConfigDialog(view_model_mock)
    qtbot.addWidget(dialog)
    return dialog

def test_reset_button_clicked(config_dialog, view_model_mock, qtbot):
    view_model_mock.get_initial_data = MagicMock(return_value={"some": "data"})
    config_dialog.mapper.export_to_ui = MagicMock()

    reset_btn = config_dialog.ui.buttonBox.button(QDialogButtonBox.Reset)
    qtbot.mouseClick(reset_btn, Qt.LeftButton)

    view_model_mock.get_initial_data.assert_called_once()
    config_dialog.mapper.export_to_ui.assert_called_once_with({"some": "data"}, config_dialog.ui)

def test_save_button_validation_failed(config_dialog, view_model_mock, qtbot):
    config_dialog.mapper.clear_highlights = MagicMock()
    config_dialog.mapper.update_from_ui = MagicMock(return_value={"raw": "data"})
    config_dialog.mapper.highlight_errors = MagicMock()

    def mock_apply_config(data):
        view_model_mock.validation_failed.emit({"field": "error"}, ["Global error"])
        
    view_model_mock.apply_config = MagicMock(side_effect=mock_apply_config)

    config_dialog.show()
    qtbot.waitExposed(config_dialog)

    save_btn = config_dialog.ui.buttonBox.button(QDialogButtonBox.Save)
    qtbot.mouseClick(save_btn, Qt.LeftButton)

    view_model_mock.apply_config.assert_called_once_with({"raw": "data"})
    config_dialog.mapper.highlight_errors.assert_called_once()
    
    # Dialog should remain open
    assert config_dialog.isVisible()

def test_save_button_success(config_dialog, view_model_mock, qtbot):
    config_dialog.mapper.clear_highlights = MagicMock()
    config_dialog.mapper.update_from_ui = MagicMock(return_value={"raw": "data"})
    
    def mock_apply_config(data):
        view_model_mock.config_saved.emit()

    view_model_mock.apply_config = MagicMock(side_effect=mock_apply_config)

    config_dialog.show()
    qtbot.waitExposed(config_dialog)

    save_btn = config_dialog.ui.buttonBox.button(QDialogButtonBox.Save)
    qtbot.mouseClick(save_btn, Qt.LeftButton)

    # Dialog should be closed / accepted
    assert not config_dialog.isVisible()

def test_close_button_clicked(config_dialog, qtbot):
    config_dialog.show()
    qtbot.waitExposed(config_dialog)

    close_btn = config_dialog.ui.buttonBox.button(QDialogButtonBox.Close)
    qtbot.mouseClick(close_btn, Qt.LeftButton)

    assert not config_dialog.isVisible()

def test_open_button_clicked(config_dialog, view_model_mock, qtbot, monkeypatch):
    open_btn = config_dialog.ui.buttonBox.button(QDialogButtonBox.Open)
    
    # Mock getOpenFileName to return a dummy path
    mock_getOpenFileName = MagicMock(return_value=("dummy_path.json", "JSON Files (*.json)"))
    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_getOpenFileName)
    
    # Mock load_config_from_file to verify it's called
    view_model_mock.load_config_from_file = MagicMock()
    
    qtbot.mouseClick(open_btn, Qt.LeftButton)
    
    mock_getOpenFileName.assert_called_once()
    view_model_mock.load_config_from_file.assert_called_once_with("dummy_path.json")
