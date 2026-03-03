from typing import Protocol, List
from desktop_client.presentation.state.app_state import AppState

class IMainViewModel(Protocol):
    """
    Interface for the Main Window's ViewModel.
    Applying DIP: MainWindow depends on this abstraction, not on MainViewModel directly.
    """

    @property
    def app_state(self) -> AppState:
        """Returns the reactive application state container."""
        ...

    def toggle_session(self) -> None:
        """Starts or stops the telemetry session depending on current state."""
        ...

    def shutdown(self) -> None:
        """Performs graceful shutdown; schedules async stop if session is active."""
        ...


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

class IConfigRepository(Protocol):
    """
    Interface for handling loading and saving of the application configuration data,
    decoupling file system I/O from the ViewModels.
    """
    def get_last_config_path(self) -> str:
        """Returns the absolute file path for the last saved config."""
        ...

    def save_config(self, config_data: dict) -> str:
        """
        Saves the config data as JSON and returns the file path it was saved to.
        Raises an exception if saving fails.
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

class ITelemetryManager(Protocol):
    """
    Interface for the telemetry session manager.
    Coordinates telemetry pipeline start/stop.
    """
    async def start_session(self) -> None:
        ...
        
    async def stop_session(self) -> None:
        ...

class IDialogService(Protocol):
    """
    Interface for dialog navigation, abstracting UI forms away from ViewModels or main Views.
    """
    def show_config_dialog(self) -> None:
        ...

    def show_settings_dialog(self) -> None:
        ...
