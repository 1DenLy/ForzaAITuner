import asyncio
from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
import os

from desktop_client.presentation.interfaces.protocols import IConfigValidator, IConfigRepository, ITelemetryManager
from desktop_client.presentation.state.app_state import AppState
from desktop_client.presentation.state.config_state import ConfigState
from desktop_client.presentation.state.session_state import SessionState
from desktop_client.presentation.resources.strings import UIStrings

class MainViewModel(QObject):
    """
    ViewModel for the Main Window.
    Manages application state, handles user interactions, and interacts with TelemetryManager.
    """
    
    # Signals to notify the View of errors
    error_occurred = Signal(str)
    
    def __init__(self, validator: IConfigValidator, config_repo: IConfigRepository, telemetry_manager: ITelemetryManager):
        super().__init__()
        self._validator = validator
        self._config_repo = config_repo
        
        # Instantiate AppState with reactive properties
        self.app_state = AppState(self)
        self._current_config_path: Optional[str] = None
        
        self._telemetry_manager = telemetry_manager
        
    @Slot(str)
    def load_config(self, file_path: str):
        """
        Validates and loads a configuration file.
        Transitions state to READY if successful, or emits error if failed.
        """
        if self.app_state.session_state in (SessionState.RECORDING, SessionState.FLUSHING):
            self.error_occurred.emit("Cannot load config while session is active.")
            return

        validation_errors = self._validator.validate(file_path)
        
        if validation_errors:
            error_msg = "\n".join(validation_errors)
            self.error_occurred.emit(error_msg)
            self.app_state.config_state = ConfigState.INVALID
        else:
            self._current_config_path = file_path
            self.app_state.config_state = ConfigState.READY

    @Slot()
    def load_last_config(self):
        """Attempts to load the last used configuration via the repository."""
        path = self._config_repo.get_last_config_path()
        if not path or not os.path.exists(path):
            raise FileNotFoundError("Last configuration not found. Please setup config manually.")
        self.load_config(path)

    def validate_and_apply_config(self, config_data: dict):
        """
        Saves the provided dict to the configuration repository and validates it.
        This provides a bridge for dynamically generated configs from UI dialogs.
        """
        try:
            path = self._config_repo.save_config(config_data)
            self.load_config(path)
        except (IOError, ValueError) as e:
            self.error_occurred.emit(f"Failed to apply config: {str(e)}")
            self.app_state.config_state = ConfigState.INVALID

    @Slot()
    def toggle_session(self):
        """
        Starts or stops the session depending on the current state.
        Schedules the appropriate async coroutine on the running event loop
        (unified Qt+asyncio via qasync).
        """
        loop = asyncio.get_event_loop()
        if self.app_state.session_state == SessionState.IDLE and self.app_state.config_state == ConfigState.READY:
            loop.create_task(self.start_recording())
        elif self.app_state.session_state == SessionState.RECORDING:
            loop.create_task(self.stop_recording())

    async def start_recording(self):
        """
        Stage 2: Session Flow (Happy Path)
        Changes state to STARTING, calls TelemetryManager, then changes to RECORDING.
        """
        try:
            self.app_state.session_state = SessionState.STARTING
            await self._telemetry_manager.start_session()
            self.app_state.session_state = SessionState.RECORDING
        except (ConnectionError, OSError, TimeoutError, ValueError) as e:
            # Expected domain errors: network/IO problems or bad telemetry config.
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format(str(e)))
            self.app_state.session_state = SessionState.IDLE
        except Exception:
            # Unexpected exceptions (e.g. programming errors) must not be silenced.
            self.app_state.session_state = SessionState.IDLE
            raise

    async def stop_recording(self):
        """
        Stage 3: Stop & Flush Flow
        Changes state to FLUSHING, stops TelemetryManager, then changes to IDLE.
        """
        try:
            self.app_state.session_state = SessionState.FLUSHING
            await self._telemetry_manager.stop_session()
            self.app_state.session_state = SessionState.IDLE
        except (ConnectionError, OSError, TimeoutError, ValueError) as e:
            # Expected domain errors during flush/stop.
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format(str(e)))
            self.app_state.session_state = SessionState.IDLE
        except Exception:
            # Re-raise programming errors so they surface in logs/crash reporters.
            self.app_state.session_state = SessionState.IDLE
            raise

    def shutdown(self):
        """
        Graceful shutdown handling. Schedules stop_recording on the running event loop.
        """
        if self.app_state.session_state in (SessionState.RECORDING, SessionState.STARTING):
            loop = asyncio.get_event_loop()
            loop.create_task(self.stop_recording())
