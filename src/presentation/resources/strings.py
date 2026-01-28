"""
Centralized storage for all user-facing strings in the Presentation Layer.
Prevents "magic strings" in code and simplifies localization.
"""

class UIStrings:
    # Error Messages
    ERR_INVALID_JSON_FORMAT = "Invalid JSON format: {}"
    ERR_MISSING_FIELD = "Missing required field: '{}'"
    ERR_VALUE_OUT_OF_RANGE = "Value for '{}' is out of range. Expected {} - {}."
    ERR_FILE_NOT_FOUND = "Configuration file not found: {}"
    ERR_GENERIC = "An unexpected error occurred: {}"
    
    # Dialog Titles
    TITLE_ERROR = "Error"
    TITLE_INFO = "Information"
    TITLE_SELECT_CONFIG = "Select Configuration File"

    # Status Messages
    STATUS_IDLE = "Idle"
    STATUS_READY = "Ready to Start"
    STATUS_RACING = "Session in Progress..."
    STATUS_SAVING = "Saving Data..."
    STATUS_ERROR = "Error Occurred"

    # Button Labels
    BTN_START = "Start Session"
    BTN_STOP = "Stop Session"
    BTN_LOAD_CONFIG = "Load Config"
