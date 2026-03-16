from typing import Protocol, Any
from desktop_client.application.state import SessionFlowManager, ConfigFlowManager


class IMainViewModel(Protocol):
    """
    Interface for the Main Window's ViewModel.
    Applying DIP: MainWindow depends on this abstraction, not on MainViewModel directly.
    """

    @property
    def session_flow(self) -> SessionFlowManager:
        """Returns the session flow manager."""
        ...

    @property
    def config_flow(self) -> ConfigFlowManager:
        """Returns the config flow manager."""
        ...

    def toggle_session(self) -> None:
        """Starts or stops the telemetry session depending on current state."""
        ...

    def shutdown(self) -> None:
        """Performs graceful shutdown; schedules async stop if session is active."""
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

    def get_last_valid_config(self) -> dict[str, Any]:
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
