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
    TITLE_PRESET_LOADED = "Preset loaded"
    TITLE_VALIDATION_ERROR = "Validation error"
    TITLE_SAVING_ERROR = "Saving error"

    # Status Messages
    STATUS_IDLE = "Idle"
    STATUS_READY = "Ready to Start"
    STATUS_STARTING = "Starting..."
    STATUS_RACING = "Session in Progress..."
    STATUS_SAVING = "Saving Data..."
    STATUS_ERROR = "Error Occurred"

    # User Feedback Messages
    MSG_PRESET_LOAD_SUCCESS = "Preset loaded successfully!\nDon't forget to click 'Save' to apply it."
    MSG_VALIDATION_FAILED_PREFIX = "Invalid data detected:\n\n"

    # File Dialog Captions
    CAPTION_OPEN_PRESET = "Open preset"
    FILE_FILTER_JSON = "JSON Files (*.json)"

    # Button Labels
    BTN_START = "Start Session"
    BTN_STOP = "Stop Session"
    BTN_LOAD_CONFIG = "Load Config"
