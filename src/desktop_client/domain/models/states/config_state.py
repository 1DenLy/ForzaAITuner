from enum import StrEnum, auto

class ConfigState(StrEnum):
    """
    Represents the state of the configuration editor/form.
    """
    LOADING = auto()      # Preparing data for the form
    EDITING = auto()      # Interactive interaction
    VALIDATING = auto()   # Validation of business rules
    SAVING = auto()       # Persisting changes
    READY = auto()        # Terminal state: config is valid and ready for use
    EMPTY = auto()        # No configuration loaded
    INVALID = auto()      # Configuration is invalid
