from typing import Protocol, Any
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


class IConfigViewModel(Protocol):
    """
    Interface for the Config Dialog's ViewModel.
    Applying DIP: ConfigDialog depends on this abstraction.
    """
    # Signals (type-hinted as Any for Protocol compatibility)
    validation_failed: Any
    preset_loaded: Any
    config_saved: Any
    global_error_occurred: Any

    def get_initial_data(self) -> dict[str, Any]:
        ...

    def apply_config(self, raw_data_dict: dict[str, Any]) -> None:
        ...

    def load_config_from_file(self, filepath: str) -> None:
        ...


class IPresetRepository(Protocol):
    """
    Interface for reading configuration presets from storage.
    Applying SRP: ViewModel delegates file I/O to this abstraction.
    """
    def load_preset(self, filepath: str) -> str:
        """Loads a preset file and returns its raw JSON content."""
        ...
