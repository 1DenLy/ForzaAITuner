from PySide6.QtCore import QObject, Signal, Property

from .config_state import ConfigState
from .session_state import SessionState

class AppState(QObject):
    """
    Global application state container.
    Provides reactive properties (signals via PySide) for UI updates.
    """
    config_state_changed = Signal(ConfigState)
    session_state_changed = Signal(SessionState)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config_state = ConfigState.EMPTY
        self._session_state = SessionState.IDLE

    @Property(ConfigState, notify=config_state_changed)
    def config_state(self) -> ConfigState:
        return self._config_state

    @config_state.setter
    def config_state(self, new_state: ConfigState):
        if self._config_state != new_state:
            self._config_state = new_state
            self.config_state_changed.emit(new_state)

    @Property(SessionState, notify=session_state_changed)
    def session_state(self) -> SessionState:
        return self._session_state

    @session_state.setter
    def session_state(self, new_state: SessionState):
        if self._session_state != new_state:
            self._session_state = new_state
            self.session_state_changed.emit(new_state)
