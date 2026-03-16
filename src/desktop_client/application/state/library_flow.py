import structlog
from PySide6.QtCore import QObject, Signal, Property
from desktop_client.domain.models import LibraryState

logger = structlog.get_logger(__name__)

class LibraryFlowManager(QObject):
    """
    Manages the configuration library state and flow.
    """
    state_changed = Signal(LibraryState)

    _VALID_TRANSITIONS = {
        LibraryState.INITIALIZING: [LibraryState.VIEWING],
        LibraryState.VIEWING: [
            LibraryState.EDITOR_INVOCATION,
            LibraryState.DELETING,
            LibraryState.IMPORTING_EXPORTING
        ],
        LibraryState.EDITOR_INVOCATION: [LibraryState.VIEWING],
        LibraryState.DELETING: [LibraryState.VIEWING],
        LibraryState.IMPORTING_EXPORTING: [LibraryState.VIEWING]
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = LibraryState.INITIALIZING

    @Property(LibraryState, notify=state_changed)
    def state(self) -> LibraryState:
        return self._state

    def set_state(self, new_state: LibraryState):
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

    def _is_valid_transition(self, current: LibraryState, next_state: LibraryState) -> bool:
        return next_state in self._VALID_TRANSITIONS.get(current, [])
