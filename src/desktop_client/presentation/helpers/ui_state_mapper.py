from dataclasses import dataclass
from typing import Optional

from desktop_client.domain.models import SessionState, ConfigState
from desktop_client.presentation.resources.strings import UIStrings


@dataclass(frozen=True, slots=True)
class ButtonConfig:
    """
    Immutable snapshot of a button's visual/interactive state.
    Produced by UIStateMapper so the View never needs conditional logic.
    """
    text: Optional[str]   # None means "do not change the label"
    enabled: bool


class UIStateMapper:
    """
    Presentation-layer service that maps application states to UI configuration.

    Open/Closed Principle — adding a new SessionState only requires extending
    the lookup dictionaries here; MainWindow stays untouched.
    """

    # ------------------------------------------------------------------ #
    #  Status label                                                        #
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_session_status_text(state: SessionState) -> str:
        status_map: dict[SessionState, str] = {
            SessionState.IDLE:      UIStrings.STATUS_IDLE,
            SessionState.STARTING:  UIStrings.STATUS_STARTING,
            SessionState.RECORDING: UIStrings.STATUS_RACING,
            SessionState.FLUSHING:      UIStrings.STATUS_SAVING,
            SessionState.FLUSHING_EXIT: UIStrings.STATUS_SAVING,
            SessionState.ERROR:         UIStrings.STATUS_ERROR,
        }
        return status_map.get(state, "")

    # ------------------------------------------------------------------ #
    #  Start / Stop button                                                 #
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_start_button_config(
        session_state: SessionState,
        config_state: ConfigState,
    ) -> ButtonConfig:
        """
        Returns the full visual configuration for the Start/Stop button.

        Rules (mirrors the original if/elif logic, but centralised):
          - RECORDING          → "Stop Session",  enabled
          - IDLE + READY       → "Start Session", enabled
          - STARTING/FLUSHING  → any text,        disabled
          - IDLE + not READY   → "Start Session", disabled
        """
        if session_state == SessionState.RECORDING:
            return ButtonConfig(text=UIStrings.BTN_STOP, enabled=True)

        if session_state == SessionState.IDLE and config_state == ConfigState.READY:
            return ButtonConfig(text=UIStrings.BTN_START, enabled=True)

        # STARTING, FLUSHING — or IDLE without a valid config
        return ButtonConfig(text=UIStrings.BTN_START, enabled=False)

    # ------------------------------------------------------------------ #
    #  Config button                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_config_button_config(session_state: SessionState) -> ButtonConfig:
        """
        Returns the full visual configuration for the Load Config button.
        Config loading is only allowed while the session is idle.
        """
        return ButtonConfig(text=None, enabled=(session_state == SessionState.IDLE))
