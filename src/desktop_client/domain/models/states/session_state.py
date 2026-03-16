from enum import StrEnum, auto

class SessionState(StrEnum):
    """
    Represents the state of the telemetry recording session.
    Managed by Core and monitored by UI.
    """
    IDLE = auto()      # Session is idle, waiting to start
    STARTING = auto()  # Session starting, pipeline getting ready
    RECORDING = auto() # Session in progress, recording telemetry
    FLUSHING = auto()  # Session stopped, saving/uploading data
    FLUSHING_EXIT = auto() # Session stopping due to application exit
    ERROR = auto()     # Session encountered an error
