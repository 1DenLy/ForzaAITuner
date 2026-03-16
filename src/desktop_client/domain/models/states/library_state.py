from enum import StrEnum, auto

class LibraryState(StrEnum):
    """
    Represents the state of the configuration library.
    """
    INITIALIZING = auto()        # Initial loading of the list
    VIEWING = auto()             # Main screen, idle/filtering/sorting
    EDITOR_INVOCATION = auto()    # Preparing data for the config dialog
    DELETING = auto()            # Deleting a config file
    IMPORTING_EXPORTING = auto()  # Working with file system dialogs
