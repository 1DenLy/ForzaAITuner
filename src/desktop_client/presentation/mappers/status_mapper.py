from desktop_client.domain.models import SessionState
from desktop_client.presentation.resources.strings import UIStrings

class PresentationMapper:
    """
    Maps domain states to UI-friendly representation.
    Addresses OCP by centralizing state-to-string mapping.
    """
    
    _SESSION_STATUS_MAP = {
        SessionState.IDLE: UIStrings.STATUS_IDLE,
        SessionState.STARTING: UIStrings.STATUS_STARTING,
        SessionState.RECORDING: UIStrings.STATUS_RACING,
        SessionState.FLUSHING: UIStrings.STATUS_SAVING,
        SessionState.FLUSHING_EXIT: UIStrings.STATUS_SAVING,
        SessionState.ERROR: UIStrings.STATUS_ERROR
    }

    @staticmethod
    def to_status_string(state: SessionState) -> str:
        """Returns localized status text for a given session state."""
        return PresentationMapper._SESSION_STATUS_MAP.get(state, UIStrings.STATUS_IDLE)
