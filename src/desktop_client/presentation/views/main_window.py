from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QObject
from src.presentation.services.ui_loader_service import UiLoaderService
from src.presentation.viewmodels.main_vm import MainViewModel
from src.presentation.state.app_state import ApplicationState
from src.presentation.resources.strings import UIStrings

class BaseWindow(QMainWindow):
    """
    Base window class that manages UI loading via UiLoaderService.
    Encapsulates the loaded UI widget.
    """
    def __init__(self, ui_file_path: str):
        super().__init__()
        # Load the UI content
        self._ui_widget = UiLoaderService.load_ui(ui_file_path)
        
        if isinstance(self._ui_widget, QMainWindow):
             self.setCentralWidget(self._ui_widget)
        else:
             self.setCentralWidget(self._ui_widget)

    @property
    def ui(self):
        """Access the raw loaded UI object."""
        return self._ui_widget

    def __getattr__(self, name):
        """Delegate attribute access to the loaded UI object safely."""
        if self._ui_widget:
            if hasattr(self._ui_widget, name):
                return getattr(self._ui_widget, name)
            child = self._ui_widget.findChild(QObject, name)
            if child:
                return child
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


class MainWindow(BaseWindow):
    """
    Main Application Window.
    Binds UI events to the MainViewModel.
    """
    def __init__(self, ui_path: str, view_model: MainViewModel):
        super().__init__(ui_path)
        self._vm = view_model
        
        self._setup_connections()
        self._update_ui_state(self._vm.state) # Initial state

    def _setup_connections(self):
        # 1. View -> ViewModel
        # Assuming UI has 'pushButton_Config' and 'pushButton_Start'
        # We need to defensively check if they exist because UI is dynamic
        if hasattr(self, 'pushButton_Config'):
            self.pushButton_Config.clicked.connect(self._on_load_config_clicked)
        
        if hasattr(self, 'pushButton_Start'):
            self.pushButton_Start.clicked.connect(self._on_toggle_session_clicked)
        
        if hasattr(self, 'pushButton_Exit'):
            self.pushButton_Exit.clicked.connect(self.close)

        # 2. ViewModel -> View
        self._vm.state_changed.connect(self._update_ui_state)
        self._vm.error_occurred.connect(self._show_error)

    def _on_load_config_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            UIStrings.TITLE_SELECT_CONFIG, 
            "", 
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self._vm.load_config(file_path)

    def _on_toggle_session_clicked(self):
        self._vm.toggle_session()

    def _update_ui_state(self, state: ApplicationState):
        """
        Updates UI elements based on the current application state.
        """
        # Example logic - adapt to actual UI element names
        
        # Update Status Label if exists
        if hasattr(self, 'lbl_status'):
            status_map = {
                ApplicationState.IDLE: UIStrings.STATUS_IDLE,
                ApplicationState.READY: UIStrings.STATUS_READY,
                ApplicationState.RACING: UIStrings.STATUS_RACING,
                ApplicationState.SAVING: UIStrings.STATUS_SAVING,
                ApplicationState.ERROR: UIStrings.STATUS_ERROR
            }
            self.lbl_status.setText(status_map.get(state, ""))

        # Update Buttons
        if hasattr(self, 'pushButton_Start'):
            if state == ApplicationState.RACING:
                self.pushButton_Start.setText(UIStrings.BTN_STOP)
                self.pushButton_Start.setEnabled(True)
            elif state == ApplicationState.READY:
                self.pushButton_Start.setText(UIStrings.BTN_START)
                self.pushButton_Start.setEnabled(True)
            else:
                self.pushButton_Start.setEnabled(False) # Disable if IDLE or ERROR or SAVING

        if hasattr(self, 'pushButton_Config'):
            # Disable config loading while racing
            self.pushButton_Config.setEnabled(state not in (ApplicationState.RACING, ApplicationState.SAVING))

    def _show_error(self, message: str):
        QMessageBox.critical(self, UIStrings.TITLE_ERROR, message)

    def closeEvent(self, event):
        """
        Handle Graceful Shutdown.
        """
        if self._vm.state == ApplicationState.RACING:
            # If racing, we should stop first
            # Option A: Block close, tell user to stop
            # Option B: Auto-stop (Graceful)
            self._vm.shutdown()
            
        # Ensure cleanup happens
        self._vm.shutdown()
        event.accept()
