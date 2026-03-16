import asyncio
import logging

_logger = logging.getLogger(__name__)
from PySide6.QtCore import QObject, Signal

from desktop_client.domain.interface.interfaces import ITelemetryManager
from desktop_client.application.state import SessionFlowManager, MainFlowManager
from desktop_client.domain.models import SessionState, MainState
from desktop_client.presentation.resources.strings import UIStrings


class MainViewModel(QObject):
    """
    ViewModel for the Main Window.
    Manages session state and delegates telemetry lifecycle to TelemetryManager.

    Config readiness is driven reactively via subscribe() on ConfigDataManager
    (wired in the composition root), not handled here directly.
    """

    # Signal to notify the View of errors
    error_occurred = Signal(str)

    def __init__(
        self,
        telemetry_manager: ITelemetryManager,
        session_flow: SessionFlowManager,
        main_flow: MainFlowManager
    ) -> None:
        super().__init__()
        self._telemetry_manager = telemetry_manager
        self._session_flow = session_flow
        self._main_flow = main_flow
        self._background_tasks: set[asyncio.Task] = set()

    @property
    def session_flow(self) -> SessionFlowManager:
        return self._session_flow

    @property
    def main_flow(self) -> MainFlowManager:
        return self._main_flow

    # ------------------------------------------------------------------ #
    #  Session control                                                      #
    # ------------------------------------------------------------------ #

    def toggle_session(self) -> None:
        """
        Starts or stops the session depending on the current state.
        Schedules the appropriate async coroutine on the running event loop
        (unified Qt+asyncio via qasync).
        """
        loop = asyncio.get_event_loop()
        if (self._session_flow.state in (SessionState.IDLE, SessionState.ERROR)
                and self._main_flow.state == MainState.READY_TO_START):
            task = loop.create_task(self.start_recording())
            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)
        elif self._session_flow.state == SessionState.RECORDING:
            task = loop.create_task(self.stop_recording())
            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)

    async def start_recording(self) -> None:
        """
        Stage 2: Session Flow (Happy Path)
        Changes state to STARTING, calls TelemetryManager, then changes to RECORDING.
        """
        try:
            self._session_flow.set_state(SessionState.STARTING)
            await self._telemetry_manager.start_session()
            self._session_flow.set_state(SessionState.RECORDING)
        except (ConnectionError, OSError, TimeoutError, ValueError) as e:
            # Expected domain errors: network/IO problems or bad telemetry config.
            _logger.error(f"start_recording: expected domain error: {e}", exc_info=True)
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format("Network or system connection problem."))
            self._session_flow.set_state(SessionState.ERROR)
        except Exception as e:
            # Unexpected programming error inside a fire-and-forget task.
            _logger.error("start_recording: unexpected error", exc_info=True)
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format("Internal application error."))
            self._session_flow.set_state(SessionState.ERROR)

    async def stop_recording(self) -> None:
        """
        Stage 3: Stop & Flush Flow
        Changes state to FLUSHING, stops TelemetryManager, then changes to IDLE.
        """
        try:
            self._session_flow.set_state(SessionState.FLUSHING)
            await self._telemetry_manager.stop_session()
            self._session_flow.set_state(SessionState.IDLE)
        except (ConnectionError, OSError, TimeoutError, ValueError) as e:
            # Expected domain errors during flush/stop.
            _logger.error(f"stop_recording: expected domain error: {e}", exc_info=True)
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format("Failed to stop session cleanly."))
            self._session_flow.set_state(SessionState.ERROR)
        except Exception as e:
            # Unexpected programming error inside a fire-and-forget task.
            _logger.error("stop_recording: unexpected error", exc_info=True)
            self.error_occurred.emit(UIStrings.ERR_GENERIC.format("Internal error during session stop."))
            self._session_flow.set_state(SessionState.ERROR)

    def shutdown(self) -> None:
        """
        Graceful shutdown handling. Schedules stop_recording on the running event loop.
        """
        if self._session_flow.state in (SessionState.RECORDING, SessionState.STARTING):
            loop = asyncio.get_event_loop()
            task = loop.create_task(self.stop_recording())
            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)
