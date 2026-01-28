from PySide6.QtCore import QObject, Signal, Slot
from typing import Optional

from src.presentation.interfaces.protocols import ICoreFacade, IConfigValidator
from src.presentation.state.app_state import ApplicationState
from src.presentation.resources.strings import UIStrings

class MainViewModel(QObject):
    """
    ViewModel for the Main Window.
    Manages application state, handles user interactions, and interacts with the Core Facade.
    """
    
    # Signals to notify the View
    state_changed = Signal(ApplicationState)
    error_occurred = Signal(str)
    
    def __init__(self, core_facade: ICoreFacade, validator: IConfigValidator):
        super().__init__()
        self._core_facade = core_facade
        self._validator = validator
        
        self._state = ApplicationState.IDLE
        self._current_config_path: Optional[str] = None
        
    @property
    def state(self) -> ApplicationState:
        return self._state
        
    @state.setter
    def state(self, new_state: ApplicationState):
        if self._state != new_state:
            self._state = new_state
            self.state_changed.emit(new_state)

    @Slot(str)
    def load_config(self, file_path: str):
        """
        Validates and loads a configuration file.
        Transisions state to READY if successful, or emits error if failed.
        """
        if self.state in (ApplicationState.RACING, ApplicationState.SAVING):
            self.error_occurred.emit("Cannot load config while session is active.")
            return

        validation_errors = self._validator.validate(file_path)
        
        if validation_errors:
            # Join all errors into a single message or handle list appropriately
            # For simplicity, we join them with newlines here
            error_msg = "\n".join(validation_errors)
            self.error_occurred.emit(error_msg)
            # Ensure we don't enter ready state if failed
            self.state = ApplicationState.ERROR
        else:
            self._current_config_path = file_path
            self.state = ApplicationState.READY

    @Slot()
    def toggle_session(self):
        """
        Starts or stops the session depending on the current state.
        """
        if self.state == ApplicationState.READY:
            self._start_session()
        elif self.state == ApplicationState.RACING:
            self._stop_session()
        else:
            # Handle unexpected calls (e.g. user clicking disabled button)
            pass

    def _start_session(self):
        try:
            self._core_facade.start_tracking()
            self.state = ApplicationState.RACING
        except Exception as e:
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format(str(e)))
            self.state = ApplicationState.ERROR

    def _stop_session(self):
        try:
            self.state = ApplicationState.SAVING
            self._core_facade.stop_tracking()
            # In a real async scenario, we might wait for a 'stopped' signal from Core
            self.state = ApplicationState.READY
        except Exception as e:
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format(str(e)))
            self.state = ApplicationState.ERROR

    def shutdown(self):
        """
        Graceful shutdown handling.
        """
        if self.state == ApplicationState.RACING:
            self._core_facade.stop_tracking()
        
        self._core_facade.cleanup()
