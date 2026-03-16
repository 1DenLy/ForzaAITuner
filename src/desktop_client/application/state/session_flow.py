import structlog
from PySide6.QtCore import QObject, Signal, Property
from desktop_client.domain.models import SessionState

logger = structlog.get_logger(__name__)

class SessionFlowManager(QObject):
    """
    Manages the telemetry session lifecycle.
    Controls transitions between IDLE, STARTING, RECORDING, and FLUSHING.
    """
    state_changed = Signal(SessionState)

    _VALID_TRANSITIONS = {
        SessionState.IDLE: [SessionState.STARTING],
        SessionState.STARTING: [SessionState.RECORDING, SessionState.IDLE, SessionState.ERROR],
        SessionState.RECORDING: [SessionState.FLUSHING, SessionState.FLUSHING_EXIT, SessionState.ERROR],
        SessionState.FLUSHING: [SessionState.IDLE, SessionState.ERROR],
        SessionState.FLUSHING_EXIT: [], # Terminal
        SessionState.ERROR: [SessionState.IDLE, SessionState.STARTING]
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = SessionState.IDLE

    @Property(SessionState, notify=state_changed)
    def state(self) -> SessionState:
        return self._state

    def set_state(self, new_state: SessionState):
        """
        Transition to a new state with validation.
        """
        if self._state == new_state:
            return

        if self._is_valid_transition(self._state, new_state):
            self._state = new_state
            self.state_changed.emit(new_state)
        else:
            msg = f"Invalid state transition: {self._state.name} -> {new_state.name}"
            logger.warning("state_transition_blocked", current_state=self._state.name, requested_state=new_state.name)
            
            if __debug__:
                raise RuntimeError(msg)

    def _is_valid_transition(self, current: SessionState, next_state: SessionState) -> bool:
        return next_state in self._VALID_TRANSITIONS.get(current, [])
