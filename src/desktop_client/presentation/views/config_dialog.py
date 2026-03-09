# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QWidget, QFileDialog
from PySide6.QtCore import SIGNAL

from desktop_client.presentation.viewmodels.config_viewmodel import ConfigViewModel
from desktop_client.presentation.ui_gen.ui_config_dialog import Ui_ConfigDialog
from desktop_client.presentation.mappers.tuning_binder import TuningMapper


class ConfigDialog(QDialog):
    """
    Окно конфигурации (View), использующее сгенерированный UI (ui_config_dialog.py).
    Связывается с ConfigViewModel для валидации и передачи данных.
    """

    def __init__(self, view_model: ConfigViewModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.vm = view_model

        # ── Initialize Mapper ───────────────────────────────────────────
        self.mapper = TuningMapper()

        # ── Load UI ──────────────────────────────────
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)


        # ── Setup widgets and signals ─────────────────────────────────────
        self.mapper.populate_combo_boxes(self.ui)   # 1. populate list combo boxes
        self.mapper.configure_ranges(self.ui)       # 2. min/max/default from domain
        self.mapper.setup_slider_labels(self.ui)    # 3. connect label to valueChanged
        self._connect_signals()
        self._populate_initial_data()               # 4. load real data

    # ------------------------------------------------------------------ #
    # Setup & Initialization Methods                                     #
    # ------------------------------------------------------------------ #


    def _connect_signals(self) -> None:
        """Connects View and ViewModel, as well as dialog buttons."""
        # Disconnect standard signals for custom routing
        if self.ui.buttonBox.receivers(SIGNAL('accepted()')) > 0:
            self.ui.buttonBox.accepted.disconnect()
        if self.ui.buttonBox.receivers(SIGNAL('rejected()')) > 0:
            self.ui.buttonBox.rejected.disconnect()

        # --- QDialogButtonBox buttons ---
        save_button = self.ui.buttonBox.button(QDialogButtonBox.Save)
        if save_button:
            save_button.clicked.connect(self._on_save_clicked)

        reset_button = self.ui.buttonBox.button(QDialogButtonBox.Reset)
        if reset_button:
            reset_button.clicked.connect(self._populate_initial_data)

        close_button = self.ui.buttonBox.button(QDialogButtonBox.Close)
        if close_button:
            close_button.clicked.connect(self.reject)

        open_button = self.ui.buttonBox.button(QDialogButtonBox.Open)
        if open_button:
            open_button.clicked.connect(self._on_open_preset_clicked)

        # --- ViewModel -> View signals ---
        self.vm.validation_failed.connect(self._on_validation_failed)
        self.vm.preset_loaded.connect(self._on_preset_loaded)
        self.vm.config_saved.connect(self.accept)
        self.vm.global_error_occurred.connect(self._on_global_error)

    def _populate_initial_data(self) -> None:
        """Fills UI with current values from ViewModel."""
        model_data = self.vm.get_initial_data()
        self.mapper.export_to_ui(model_data, self.ui)

    # ------------------------------------------------------------------ #
    # Event Handlers                                                     #
    # ------------------------------------------------------------------ #

    def _on_save_clicked(self) -> None:
        """Save button handler — collects data and passes it to ViewModel."""
        # Clear error highlights before new attempt
        self.mapper.clear_highlights(self.ui)
        raw_form_data = self.mapper.update_from_ui(self.ui)
        self.vm.apply_config(raw_form_data)

    def _on_open_preset_clicked(self) -> None:
        """
        Open button handler (Load preset).
        """
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            caption="Open preset",
            filter="JSON Files (*.json)"
        )
        if filepath:
            self.vm.load_config_from_file(filepath)

    def _on_preset_loaded(self, preset_data: dict[str, Any]) -> None:
        """Fills UI with data loaded from file."""
        self.mapper.export_to_ui(preset_data, self.ui)
        QMessageBox.information(
            self, 
            "Preset loaded", 
            "Preset loaded successfully!\nDon't forget to click 'Save' to apply it."
        )

    def _on_validation_failed(self, field_errors: dict[str, str], global_errors: list[str]) -> None:
        """
        Validation failed signal handler from ViewModel.
        """
        self.mapper.highlight_errors(self.ui, field_errors)

        if global_errors:
            error_lines = [f"• {msg}" for msg in global_errors]
            QMessageBox.warning(
                self,
                "Validation error",
                "Invalid data detected:\n\n" + "\n".join(error_lines),
            )

    def _on_global_error(self, message: str) -> None:
        """Critical error (e.g., ConfigLockedError)."""
        QMessageBox.critical(self, "Saving error", message)
