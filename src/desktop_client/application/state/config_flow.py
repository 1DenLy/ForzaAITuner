import structlog
from PySide6.QtCore import QObject, Signal, Property
from desktop_client.domain.models import ConfigState

logger = structlog.get_logger(__name__)

class ConfigFlowManager(QObject):
    """
    Manages the configuration editor state and flow.
    """
    state_changed = Signal(ConfigState)

    _VALID_TRANSITIONS = {
        ConfigState.EMPTY: [ConfigState.LOADING],
        ConfigState.LOADING: [ConfigState.EDITING, ConfigState.INVALID],
        ConfigState.EDITING: [ConfigState.VALIDATING, ConfigState.EMPTY, ConfigState.LOADING],
        ConfigState.VALIDATING: [ConfigState.SAVING, ConfigState.EDITING, ConfigState.INVALID],
        ConfigState.SAVING: [ConfigState.READY, ConfigState.EDITING, ConfigState.INVALID],
        ConfigState.READY: [ConfigState.EDITING, ConfigState.LOADING, ConfigState.EMPTY],
        ConfigState.INVALID: [ConfigState.EDITING, ConfigState.LOADING, ConfigState.EMPTY]
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = ConfigState.EMPTY

    @Property(ConfigState, notify=state_changed)
    def state(self) -> ConfigState:
        return self._state

    def set_state(self, new_state: ConfigState):
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

    def _is_valid_transition(self, current: ConfigState, next_state: ConfigState) -> bool:
        return next_state in self._VALID_TRANSITIONS.get(current, [])
