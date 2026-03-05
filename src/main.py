# Standard library imports
import asyncio
import logging
import signal
import sys

# Third-party imports
import qasync
from PySide6.QtWidgets import QApplication

# Application configuration
from config import BASE_DIR, get_settings

# Domain & Infrastructure layer
from desktop_client.domain.tuning import TuningSetup
from desktop_client.infrastructure.local_config_repository import LocalConfigRepository

# Application layer & Services
from desktop_client.application.config_state_manager import ConfigStateManager
from desktop_client.application.config_validator_service import ConfigValidatorService
from desktop_client.services.telemetry_manager import TelemetryManager

# Presentation layer
from desktop_client.presentation.services.dialog_service import DialogService
from desktop_client.presentation.state.config_state import ConfigState
from desktop_client.presentation.state.session_state import SessionState
from desktop_client.presentation.viewmodels.config_viewmodel import ConfigViewModel
from desktop_client.presentation.viewmodels.main_vm import MainViewModel
from desktop_client.presentation.views.main_window import MainWindow

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Sets up the environment for the application."""
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))


def bootstrap_dependencies(settings):
    """Initializes and returns the core application dependencies."""
    logger.info("Initializing services...")
    telemetry_manager = TelemetryManager(api_url=settings.network.api_url)

    logger.info("Initializing ViewModels...")
    main_vm = MainViewModel(telemetry_manager)
    
    app_config_validator = ConfigValidatorService(TuningSetup)
    local_config_repo = LocalConfigRepository(BASE_DIR)
    app_config_state_manager = ConfigStateManager(local_config_repo)
    app_config_state_manager.initialize(TuningSetup.model_validate)
    
    config_vm = ConfigViewModel(app_config_validator, app_config_state_manager)
    
    return main_vm, config_vm, app_config_state_manager


def setup_state_bridges(main_vm: MainViewModel, app_config_state_manager: ConfigStateManager):
    """Sets up the reactive bridges between view models and state managers."""
    # ── Config-state bridge ──────────────────────────────────────────────────
    # Unlock 'Start Session' when valid config is available
    def _on_config_updated(_new_config) -> None:
        main_vm.app_state.config_state = ConfigState.READY

    app_config_state_manager.subscribe(_on_config_updated)

    # Promote state if config already exists on disk
    if app_config_state_manager.get_config() is not None:
        main_vm.app_state.config_state = ConfigState.READY
        logger.info("Cold-start: persisted config found — config_state set to READY.")

    # ── Session-lock bridge ──────────────────────────────────────────────────
    # Prevent config changes mid-race (while session is active)
    _PIPELINE_ACTIVE = frozenset({
        SessionState.STARTING,
        SessionState.RECORDING,
        SessionState.FLUSHING,
    })

    def _on_session_state_changed(state: SessionState) -> None:
        app_config_state_manager.is_recording_session = state in _PIPELINE_ACTIVE

    main_vm.app_state.session_state_changed.connect(_on_session_state_changed)


async def async_main():
    """Async GUI entry point."""
    # 1. Load Configuration
    try:
        settings = get_settings()
        logger.info(f"Configuration loaded successfully. Environment: {settings.env}")
    except Exception as e:
        logger.critical(f"Failed to load configuration: {e}")
        sys.exit(1)


    # 2. Initialize Dependencies (Services & ViewModels)
    main_vm, config_vm, app_config_state_manager = bootstrap_dependencies(settings)

    # 3. Setup reactive bridges
    setup_state_bridges(main_vm, app_config_state_manager)

    # 4. Initialize Dialog Services and View (Window)
    logger.info("Initializing View...")
    dialog_service = DialogService(main_vm, config_vm)
    window = MainWindow(main_vm, dialog_service)
    dialog_service.set_main_window(window)
    window.show()

    # 5. Keep coroutine alive until Qt application quits
    future = asyncio.get_event_loop().create_future()

    def on_app_quit():
        if not future.done():
            future.set_result(None)

    QApplication.instance().aboutToQuit.connect(on_app_quit)
    await future


def main():
    """Synchronous entry point."""
    setup_environment()

    app = QApplication(sys.argv)
    app.setApplicationName("ForzaAITuner")
    app.setApplicationVersion("1.0.0")

    # Bridge Qt and asyncio event loops
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda *_: app.quit())

    try:
        with loop:
            loop.run_until_complete(async_main())
    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()