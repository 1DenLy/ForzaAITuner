"""
Application-layer port definitions (Ports & Adapters pattern).

These are the *inward-facing* interfaces that the Application layer
defines and that Infrastructure/Presentation layers must implement.

Rules:
  - No concrete implementations here.
  - No imports from infrastructure or presentation layers.
  - Infrastructure adapts TO these ports; the application layer owns them.
"""
from typing import Any, Protocol


class IConfigRepository(Protocol):
    """
    Port for configuration persistence.

    Implemented by: infrastructure.LocalConfigRepository
    Used by:        application.ConfigStateManager
    """

    def load_raw_data(self) -> dict[str, Any]:
        """Load the raw configuration dictionary from storage."""
        ...

    def save_raw_data(self, data: dict[str, Any]) -> None:
        """Persist the raw configuration dictionary to storage."""
        ...
