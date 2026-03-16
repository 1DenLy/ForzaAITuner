import structlog
from PySide6.QtCore import QObject, Signal, Property
from desktop_client.domain.models import MainState

logger = structlog.get_logger(__name__)

class MainFlowManager(QObject):
    """
    Manages the internal state of the MainWindow.
    """
    state_changed = Signal(MainState)

    _VALID_TRANSITIONS = {
        MainState.MONITORING_CONFIG: [MainState.VALID_CONFIG, MainState.ERROR],
        MainState.VALID_CONFIG: [MainState.READY_TO_START, MainState.MONITORING_CONFIG, MainState.ERROR],
        MainState.READY_TO_START: [MainState.MONITORING_CONFIG, MainState.ERROR],
        MainState.ERROR: [MainState.MONITORING_CONFIG]
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = MainState.MONITORING_CONFIG

    @Property(MainState, notify=state_changed)
    def state(self) -> MainState:
        return self._state

    def set_state(self, new_state: MainState):
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

    def _is_valid_transition(self, current: MainState, next_state: MainState) -> bool:
        return next_state in self._VALID_TRANSITIONS.get(current, [])
