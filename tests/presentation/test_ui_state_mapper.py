import pytest
from desktop_client.presentation.services.ui_state_mapper import UIStateMapper, ButtonConfig
from desktop_client.presentation.state.session_state import SessionState
from desktop_client.presentation.state.config_state import ConfigState
from desktop_client.presentation.resources.strings import UIStrings

def test_get_session_status_text():
    assert UIStateMapper.get_session_status_text(SessionState.IDLE) == UIStrings.STATUS_IDLE
    assert UIStateMapper.get_session_status_text(SessionState.STARTING) == UIStrings.STATUS_STARTING
    assert UIStateMapper.get_session_status_text(SessionState.RECORDING) == UIStrings.STATUS_RACING
    assert UIStateMapper.get_session_status_text(SessionState.FLUSHING) == UIStrings.STATUS_SAVING
    # Ensure it handles unexpected/None smoothly due to .get() behavior
    # Note: passing wrong type might happen, we just check the output 
    assert UIStateMapper.get_session_status_text(None) == ""

def test_get_start_button_config_recording():
    config = UIStateMapper.get_start_button_config(SessionState.RECORDING, ConfigState.READY)
    assert config == ButtonConfig(text=UIStrings.BTN_STOP, enabled=True)
    
def test_get_start_button_config_idle_ready():
    config = UIStateMapper.get_start_button_config(SessionState.IDLE, ConfigState.READY)
    assert config == ButtonConfig(text=UIStrings.BTN_START, enabled=True)
    
def test_get_start_button_config_starting_or_flushing():
    config_starting = UIStateMapper.get_start_button_config(SessionState.STARTING, ConfigState.READY)
    assert config_starting.enabled is False
    assert config_starting.text == UIStrings.BTN_START
    
    config_flushing = UIStateMapper.get_start_button_config(SessionState.FLUSHING, ConfigState.READY)
    assert config_flushing.enabled is False
    assert config_flushing.text == UIStrings.BTN_START

def test_get_start_button_config_idle_not_ready():
    config_empty = UIStateMapper.get_start_button_config(SessionState.IDLE, ConfigState.EMPTY)
    assert config_empty == ButtonConfig(text=UIStrings.BTN_START, enabled=False)
    
    config_invalid = UIStateMapper.get_start_button_config(SessionState.IDLE, ConfigState.INVALID)
    assert config_invalid == ButtonConfig(text=UIStrings.BTN_START, enabled=False)

def test_get_config_button_config():
    # Only enabled when IDLE
    assert UIStateMapper.get_config_button_config(SessionState.IDLE) == ButtonConfig(text=None, enabled=True)
    assert UIStateMapper.get_config_button_config(SessionState.RECORDING) == ButtonConfig(text=None, enabled=False)
    assert UIStateMapper.get_config_button_config(SessionState.STARTING) == ButtonConfig(text=None, enabled=False)
    assert UIStateMapper.get_config_button_config(SessionState.FLUSHING) == ButtonConfig(text=None, enabled=False)
