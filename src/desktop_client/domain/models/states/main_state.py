from enum import StrEnum, auto

class MainState(StrEnum):
    """
    Represents the internal state of the MainWindow, 
    independent of the core session state.
    """
    MONITORING_CONFIG = auto() # Checking for valid setup
    VALID_CONFIG = auto()     # Config is loaded and valid
    READY_TO_START = auto()   # All systems go, button enabled
    ERROR = auto()            # Critical UI or initialization error
