# -*- coding: utf-8 -*-
from __future__ import annotations

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QWidget

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

        # ── Инициализация Mapper'а ───────────────────────────────────────────
        self.mapper = TuningMapper()

        # ── Подключение сгенерированного UI ──────────────────────────────────
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)

        # ── Настройка виджетов и сигналов ─────────────────────────────────────
        self.mapper.populate_combo_boxes(self.ui)   # 1. заполнить списки из домена
        self.mapper.configure_ranges(self.ui)       # 2. min/max/default из домена
        self.mapper.setup_slider_labels(self.ui)    # 3. подключить label к valueChanged
        self._connect_signals()
        self._populate_initial_data()               # 4. загрузить реальные данные

    # ------------------------------------------------------------------ #
    # Setup & Initialization Methods                                     #
    # ------------------------------------------------------------------ #


    def _connect_signals(self) -> None:
        """Связывает View и ViewModel, а также кнопки диалога."""
        # --- Кнопки QDialogButtonBox ---
        save_button = self.ui.buttonBox.button(QDialogButtonBox.Save)
        if save_button:
            save_button.clicked.connect(self._on_save_clicked)

        # Close/Reject
        self.ui.buttonBox.rejected.connect(self.reject)

        # Reset — восстановить начальные значения
        reset_button = self.ui.buttonBox.button(QDialogButtonBox.Reset)
        if reset_button:
            reset_button.clicked.connect(self._populate_initial_data)

        # --- Сигналы ViewModel -> View ---
        self.vm.validation_failed.connect(self._on_validation_failed)
        self.vm.config_saved.connect(self.accept)
        self.vm.global_error_occurred.connect(self._on_global_error)

    def _populate_initial_data(self) -> None:
        """Заполняет UI текущими значениями из ViewModel."""
        model_data = self.vm.get_initial_data()
        self.mapper.export_to_ui(model_data, self.ui)

    # ------------------------------------------------------------------ #
    # Event Handlers                                                     #
    # ------------------------------------------------------------------ #

    def _on_save_clicked(self) -> None:
        """Обработчик кнопки Save — собирает данные и передаёт во ViewModel."""
        # Сбрасываем подсветку ошибок перед новой попыткой
        self.mapper.clear_highlights(self.ui)
        raw_form_data = self.mapper.update_from_ui(self.ui)
        self.vm.apply_config(raw_form_data)

    def _on_validation_failed(self, errors: dict[str, str]) -> None:
        """
        Обработчик сигнала validation_failed от ViewModel.

        Передаёт ошибки в TuningMapper, который подсвечивает конкретные виджеты
        красной рамкой и tootlip-подсказкой. Если поле не имеет виджета
        (напр. поле вычисляемое), оно попадает в резервный QMessageBox.
        """
        self.mapper.highlight_errors(self.ui, errors)

        # Собираем ошибки для полей, у которых нет виджета-соответствия
        bound_paths = {
            ".".join(b.model_path)
            for b in self.mapper.bindings
        }
        unmatched = {
            field: msg
            for field, msg in errors.items()
            if field not in bound_paths
        }
        if unmatched:
            error_lines = [f"• {field}: {msg}" for field, msg in unmatched.items()]
            QMessageBox.warning(
                self,
                "Ошибка валидации",
                "Обнаружены ошибки:\n\n" + "\n".join(error_lines),
            )

    def _on_global_error(self, message: str) -> None:
        """Критическая ошибка (например: ConfigLockedError)."""
        QMessageBox.critical(self, "Ошибка сохранения", message)
