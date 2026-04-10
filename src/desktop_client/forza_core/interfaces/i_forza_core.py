from typing import Protocol

class IForzaCore(Protocol):
    """
    Interface for interacting with the Forza Core logic.
    Decouples Presentation Layer from specific Core implementations.
    """
    def start_tracking(self) -> None:
        """Starts the race session tracking/recording."""
        ...

    def stop_tracking(self) -> None:
        """Stops the race session tracking."""
        ...

    def cleanup(self) -> None:
        """Performs cleanup operations (e.g. closing connections) for graceful shutdown."""
        ...

    def is_tracking(self) -> bool:
        """Returns True if a session is currently being tracked."""
        ...
