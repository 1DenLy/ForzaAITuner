from typing import Protocol, List

class IConfigValidator(Protocol):
    """
    Interface for validating configuration files.
    """
    def validate(self, file_path: str) -> List[str]:
        """
        Validates the configuration file at the given path.

        Args:
            file_path: Absolute path to the configuration file (JSON).

        Returns:
            List[str]: A list of localized error messages. Returns empty list if validation succeeds.
        """
        ...

class ICoreFacade(Protocol):
    """
    Interface for interacting with the Core Application logic.
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
