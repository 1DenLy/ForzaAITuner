from enum import Enum, auto

class SessionState(Enum):
    """
    Represents the state of the telemetry recording session as defined in docs/01_UI/States diagrams/Session State.drawio.
    """
    IDLE = auto()      # Session is idle, waiting to start
    STARTING = auto()  # Session starting, pipeline getting ready
    RECORDING = auto() # Session in progress, recording telemetry
    FLUSHING = auto()  # Session stopped, saving/uploading data
