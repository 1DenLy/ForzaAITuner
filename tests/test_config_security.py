import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from config import AIConfig, BASE_DIR, Settings, UIConfig
from main import log_secure_validation_error


class MockLogger:
    def __init__(self):
        self.messages = []

    def critical(self, msg: str):
        self.messages.append(msg)


def test_path_traversal_validation_ui():
    """Test that a malicious path is correctly caught by the Pydantic validator in UIConfig."""
    traversal_path = "../../../../../../../Windows/System32/explorer.exe"

    with pytest.raises(ValidationError) as exc_info:
        UIConfig(main_window_path=Path(traversal_path))

    errors = exc_info.value.errors(include_input=False)
    assert len(errors) > 0
    err_msg = str(errors[0]["msg"])
    assert "Path traversal detected" in err_msg or "File not found" in err_msg


def test_path_traversal_validation_ai():
    """Test that a malicious path is correctly caught by the Pydantic validator in AIConfig."""
    traversal_path = "../../../../../../../usr/bin/python"
    
    with pytest.raises(ValidationError) as exc_info:
        AIConfig(model_path=Path(traversal_path))

    errors = exc_info.value.errors(include_input=False)
    assert len(errors) > 0
    err_msg = str(errors[0]["msg"])
    assert "Path traversal detected" in err_msg or "File not found" in err_msg


def test_secure_logging_filters_sensitive_input(monkeypatch):
    """Test that ValidationError logging does not include input values."""
    # Force a validation error by providing a malicious/invalid type for the port
    monkeypatch.setenv("DB_PORT", "not-a-number")
    monkeypatch.setenv("DB_PASSWORD", "MY_SUPER_SECRET_PASSWORD")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_NAME", "mydb")

    mock_logger = MockLogger()

    with pytest.raises(ValidationError) as exc_info:
        # Load settings, this will fail on DB_PORT
        Settings()

    # Pass the actual validation error to our secure logger
    log_secure_validation_error(exc_info.value, mock_logger)

    assert len(mock_logger.messages) == 1
    log_message = mock_logger.messages[0]

    # The log message should report an issue with the db port
    assert "db -> port" in log_message
    
    # It must NOT contain the sensitive password or even the invalid input
    assert "not-a-number" not in log_message
    assert "MY_SUPER_SECRET_PASSWORD" not in log_message
