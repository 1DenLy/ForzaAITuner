from PySide6.QtWidgets import QMainWindow, QMessageBox, QPushButton, QLabel
from PySide6.QtCore import Slot

from desktop_client.presentation.interfaces.protocols import IDialogService, IMainViewModel
from desktop_client.presentation.state.config_state import ConfigState
from desktop_client.presentation.state.session_state import SessionState
from desktop_client.presentation.resources.strings import UIStrings
from desktop_client.presentation.helpers.ui_state_mapper import UIStateMapper, ButtonConfig
from desktop_client.presentation.ui.generated.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Main Application Window.

    Pure View in the MVVM pattern — contains zero business logic.
    Depends on IMainViewModel abstraction (DIP), not on the concrete MainViewModel.
    Uses AOT-compiled Ui_MainWindow for fast, type-safe UI setup.
    """

    def __init__(self, view_model: IMainViewModel, dialog_service: IDialogService):
        super().__init__()
        self._vm = view_model
        self._dialog_service = dialog_service

        # Setup AOT-compiled UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # Explicit typed widget references (replaces findChild)
        self.btn_config: QPushButton = self._ui.pushButton_Config
        self.btn_start: QPushButton = self._ui.pushButton_Start
        self.btn_settings: QPushButton = self._ui.pushButton_Settings
        self.btn_exit: QPushButton = self._ui.pushButton_Exit
        # label_3 is the "Status" label in Ui_MainWindow (objectName="label_3",
        # retranslateUi sets its text to "Status"). Using a direct typed ref
        # instead of getattr avoids the runtime-only duck-typing hack that
        # mypy and other static analysers cannot verify.
        self.lbl_status: QLabel = self._ui.label_3

        self._setup_connections()
        self._update_session_ui(self._vm.app_state.session_state)   # initial render
        self._update_config_ui(self._vm.app_state.config_state)     # initial render

    # ------------------------------------------------------------------ #
    #  Signal wiring                                                       #
    # ------------------------------------------------------------------ #

    def _setup_connections(self):
        # View → ViewModel
        if self.btn_config:
            self.btn_config.clicked.connect(self._on_load_config_clicked)

        if self.btn_start:
            self.btn_start.clicked.connect(self._on_toggle_session_clicked)

        if self.btn_settings:
            self.btn_settings.clicked.connect(self._on_settings_clicked)

        if self.btn_exit:
            self.btn_exit.clicked.connect(self.close)

        # ViewModel → View
        self._vm.app_state.session_state_changed.connect(self._update_session_ui)
        self._vm.app_state.config_state_changed.connect(self._update_config_ui)
        self._vm.error_occurred.connect(self._show_error)

    # ------------------------------------------------------------------ #
    #  Slots → ViewModel                                                   #
    # ------------------------------------------------------------------ #

    @Slot()
    def _on_load_config_clicked(self):
        self._dialog_service.show_config_dialog()

    @Slot()
    def _on_settings_clicked(self):
        self._dialog_service.show_settings_dialog()

    @Slot()
    def _on_toggle_session_clicked(self):
        self._vm.toggle_session()

    # ------------------------------------------------------------------ #
    #  Reactive state handlers (ViewModel → View)                         #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _apply_button_config(button: QPushButton | None, cfg: ButtonConfig) -> None:
        """Applies a ButtonConfig to a QPushButton. Centralises button mutation."""
        if button is None:
            return
        if cfg.text is not None:
            button.setText(cfg.text)
        button.setEnabled(cfg.enabled)

    @Slot(SessionState)
    def _update_session_ui(self, state: SessionState) -> None:
        """
        Updates UI elements based on the current session state.
        OCP-compliant: no if/elif here — all logic lives in UIStateMapper.
        Adding a new SessionState only requires updating UIStateMapper.
        """
        self.lbl_status.setText(UIStateMapper.get_session_status_text(state))

        self._apply_button_config(
            self.btn_start,
            UIStateMapper.get_start_button_config(state, self._vm.app_state.config_state),
        )
        self._apply_button_config(
            self.btn_config,
            UIStateMapper.get_config_button_config(state),
        )

    @Slot(ConfigState)
    def _update_config_ui(self, state: ConfigState) -> None:
        """
        Updates UI elements based on the current config state.
        Re-evaluates the start button using UIStateMapper to stay OCP-compliant.
        """
        self._apply_button_config(
            self.btn_start,
            UIStateMapper.get_start_button_config(self._vm.app_state.session_state, state),
        )

    @Slot(str)
    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, UIStrings.TITLE_ERROR, message)

    # ------------------------------------------------------------------ #
    #  Lifecycle                                                           #
    # ------------------------------------------------------------------ #

    def closeEvent(self, event):
        """Graceful shutdown — delegates to ViewModel."""
        self._vm.shutdown()
        event.accept()
