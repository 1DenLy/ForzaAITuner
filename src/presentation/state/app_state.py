from enum import Enum, auto

class ApplicationState(Enum):
    """
    Represents the global state of the application UI.
    """
    IDLE = auto()          # Waiting for user action, config not loaded
    READY = auto()         # Config is valid, ready to start session
    RACING = auto()        # Session in progress (recording/ingestion)
    SAVING = auto()        # Blocking UI operation (saving data)
    ERROR = auto()         # Error state (validation failed, core error)
