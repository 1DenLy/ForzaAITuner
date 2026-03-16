from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Slot

from desktop_client.presentation.viewmodels.main_vm import MainViewModel
from desktop_client.presentation.interfaces.protocols import IDialogService
from desktop_client.domain.models import MainState, SessionState
from desktop_client.presentation.resources.strings import UIStrings
from desktop_client.presentation.ui.generated.ui_main_window import Ui_MainWindow
from desktop_client.presentation.mappers.status_mapper import PresentationMapper


class MainWindow(QMainWindow):
    """
    Main Application Window.
    Dumb View: No business logic, only setupUi, action forwarding, and signal reaction.
    """

    def __init__(self, viewmodel: MainViewModel, dialog_service: IDialogService):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._vm = viewmodel
        self._dialog_service = dialog_service

        self._setup_connections()
        # Initial UI update
        self._on_session_state_changed(self._vm.session_flow.state)
        self._on_main_state_changed(self._vm.main_flow.state)

    def _setup_connections(self):
        # View -> ViewModel
        self.ui.pushButton_Config.clicked.connect(self._on_config_clicked)
        self.ui.pushButton_Start.clicked.connect(self._on_start_clicked)
        self.ui.pushButton_Settings.clicked.connect(self._on_settings_clicked)
        self.ui.pushButton_Exit.clicked.connect(self.close)

        # ViewModel -> View (Reactive state updates)
        self._vm.session_flow.state_changed.connect(self._on_session_state_changed)
        self._vm.main_flow.state_changed.connect(self._on_main_state_changed)
        self._vm.error_occurred.connect(self._show_error)

    @Slot()
    def _on_config_clicked(self):
        self._dialog_service.show_config_dialog()

    @Slot()
    def _on_start_clicked(self):
        self._vm.toggle_session()

    @Slot()
    def _on_settings_clicked(self):
        self._dialog_service.show_settings_dialog()

    @Slot(SessionState)
    def _on_session_state_changed(self, state: SessionState):
        """Update UI based on SessionState Enum."""
        # Example: Update status label and start button text/enabled state
        status_text = PresentationMapper.to_status_string(state)
        self.ui.label_3.setText(status_text)
        
        btn_text = "Stop" if state == SessionState.RECORDING else "Start"
        self.ui.pushButton_Start.setText(btn_text)
        
        self.ui.pushButton_Start.setEnabled(state in (SessionState.IDLE, SessionState.RECORDING))
        self.ui.pushButton_Config.setEnabled(state == SessionState.IDLE)

    @Slot(MainState)
    def _on_main_state_changed(self, state: MainState):
        """Update UI based on MainState Enum."""
        # Example: If not ready to start, disable start button
        if state != MainState.READY_TO_START:
             self.ui.pushButton_Start.setEnabled(False)

    @Slot(str)
    def _show_error(self, message: str):
        QMessageBox.critical(self, UIStrings.TITLE_ERROR, message)

    def closeEvent(self, event):
        self._vm.shutdown()
        event.accept()
