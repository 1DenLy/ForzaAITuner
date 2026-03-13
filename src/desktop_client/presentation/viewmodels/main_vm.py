import asyncio
import logging

_logger = logging.getLogger(__name__)
from PySide6.QtCore import QObject, Signal

from desktop_client.domain.interface.interfaces import ITelemetryManager
from desktop_client.presentation.state.app_state import AppState
from desktop_client.presentation.state.session_state import SessionState
from desktop_client.presentation.resources.strings import UIStrings


class MainViewModel(QObject):
    """
    ViewModel for the Main Window.
    Manages session state and delegates telemetry lifecycle to TelemetryManager.

    Config readiness is driven reactively via subscribe() on ConfigStateManager
    (wired in the composition root), not handled here directly.
    """

    # Signal to notify the View of errors
    error_occurred = Signal(str)

    def __init__(self, telemetry_manager: ITelemetryManager) -> None:
        super().__init__()
        self._telemetry_manager = telemetry_manager

        # Instantiate AppState with reactive properties
        self.app_state = AppState(self)

    # ------------------------------------------------------------------ #
    #  Session control                                                      #
    # ------------------------------------------------------------------ #

    def toggle_session(self) -> None:
        """
        Starts or stops the session depending on the current state.
        Schedules the appropriate async coroutine on the running event loop
        (unified Qt+asyncio via qasync).
        """
        from desktop_client.presentation.state.config_state import ConfigState
        loop = asyncio.get_event_loop()
        if (self.app_state.session_state == SessionState.IDLE
                and self.app_state.config_state == ConfigState.READY):
            loop.create_task(self.start_recording())
        elif self.app_state.session_state == SessionState.RECORDING:
            loop.create_task(self.stop_recording())

    async def start_recording(self) -> None:
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
        except Exception as e:
            # Unexpected programming error inside a fire-and-forget task.
            # `raise` here would silently rot in the asyncio event loop —
            # UI would never know and app would stay stuck in STARTING.
            _logger.error("start_recording: unexpected error", exc_info=True)
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format(str(e)))
            self.app_state.session_state = SessionState.IDLE

    async def stop_recording(self) -> None:
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
        except Exception as e:
            # Unexpected programming error inside a fire-and-forget task.
            # Same rationale as start_recording: surface via UI, not stderr.
            _logger.error("stop_recording: unexpected error", exc_info=True)
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format(str(e)))
            self.app_state.session_state = SessionState.IDLE

    def shutdown(self) -> None:
        """
        Graceful shutdown handling. Schedules stop_recording on the running event loop.
        """
        if self.app_state.session_state in (SessionState.RECORDING, SessionState.STARTING):
            loop = asyncio.get_event_loop()
            loop.create_task(self.stop_recording())
