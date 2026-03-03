from typing import Protocol
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
