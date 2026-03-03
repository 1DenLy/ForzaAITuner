from enum import Enum, auto

class ConfigState(Enum):
    """
    Represents the state of the configuration UI/form as defined in docs/01_UI/States diagrams/Config State.drawio.
    """
    EMPTY = auto()     # No configuration loaded/entered
    DRAFT = auto()     # Configuration being edited
    READY = auto()     # Configuration is valid and ready
    INVALID = auto()   # Configuration validation failed
