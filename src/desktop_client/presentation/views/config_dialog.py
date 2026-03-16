from __future__ import annotations
from typing import Any

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QWidget, QFileDialog
from PySide6.QtCore import Slot

from desktop_client.presentation.viewmodels.config_viewmodel import ConfigViewModel
from desktop_client.presentation.ui.generated.ui_config_dialog import Ui_ConfigDialog
from desktop_client.presentation.mappers.tuning_binder import TuningMapper
from desktop_client.presentation.resources.strings import UIStrings
from desktop_client.domain.models import ConfigState


class ConfigDialog(QDialog):
    """
    Configuration Dialog.
    Dumb View: No business logic, only setupUi, action forwarding, and signal reaction.
    """

    def __init__(self, viewmodel: ConfigViewModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)

        self._vm = viewmodel
        self._mapper = TuningMapper()

        self._setup_ui_logic()
        self._setup_connections()

        # Initial UI update
        self._on_state_changed(self._vm.config_flow.state)
        self._load_current_data()

    def _setup_ui_logic(self):
        """Prepare UI widgets using the mapper."""
        self._mapper.populate_combo_boxes(self.ui)
        self._mapper.configure_ranges(self.ui)
        self._mapper.setup_slider_labels(self.ui)

    def _setup_connections(self):
        # View -> ViewModel (Forward actions)
        save_btn = self.ui.buttonBox.button(QDialogButtonBox.Save)
        if save_btn:
            save_btn.clicked.connect(self._on_save_clicked)

        reset_btn = self.ui.buttonBox.button(QDialogButtonBox.Reset)
        if reset_btn:
            reset_btn.clicked.connect(self._load_current_data)

        open_btn = self.ui.buttonBox.button(QDialogButtonBox.Open)
        if open_btn:
            open_btn.clicked.connect(self._on_open_clicked)

        close_btn = self.ui.buttonBox.button(QDialogButtonBox.Close)
        if close_btn:
            close_btn.clicked.connect(self.reject)

        # ViewModel -> View (Reactive updates)
        self._vm.config_flow.state_changed.connect(self._on_state_changed)
        self._vm.validation_failed.connect(self._on_validation_failed)
        self._vm.preset_loaded.connect(self._on_preset_loaded)
        self._vm.config_saved.connect(self.accept)
        self._vm.global_error_occurred.connect(self._show_error)

    def _load_current_data(self):
        """Load current valid config into UI."""
        data = self._vm.get_last_valid_config()
        self._mapper.export_to_ui(data, self.ui)

    @Slot()
    def _on_save_clicked(self):
        self._mapper.clear_highlights(self.ui)
        data = self._mapper.update_from_ui(self.ui)
        self._vm.apply_config(data)

    @Slot()
    def _on_open_clicked(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            caption=UIStrings.CAPTION_OPEN_PRESET,
            filter=UIStrings.FILE_FILTER_JSON
        )
        if filepath:
            self._vm.load_config_from_file(filepath)

    @Slot(ConfigState)
    def _on_state_changed(self, state: ConfigState):
        """Update UI elements based on ConfigState Enum."""
        is_busy = state in (ConfigState.LOADING, ConfigState.SAVING, ConfigState.VALIDATING)
        self.setEnabled(not is_busy)
        
        # Example: show loading overlay or change cursor if busy
        # if is_busy: self.setCursor(Qt.WaitCursor)
        # else: self.setCursor(Qt.ArrowCursor)

    @Slot(dict)
    def _on_preset_loaded(self, data: dict):
        self._mapper.export_to_ui(data, self.ui)
        QMessageBox.information(self, UIStrings.TITLE_PRESET_LOADED, UIStrings.MSG_PRESET_LOAD_SUCCESS)

    @Slot(dict, list)
    def _on_validation_failed(self, field_errors: dict, global_errors: list):
        self._mapper.highlight_errors(self.ui, field_errors)
        if global_errors:
            msg = "\n".join([f"• {e}" for e in global_errors])
            QMessageBox.warning(self, UIStrings.TITLE_VALIDATION_ERROR, msg)

    @Slot(str)
    def _show_error(self, message: str):
        QMessageBox.critical(self, "Error", message)
