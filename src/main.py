import sys
import asyncio
import logging
import signal

import qasync
from PySide6.QtWidgets import QApplication

from desktop_client.presentation.views.main_window import MainWindow
from desktop_client.presentation.viewmodels.main_vm import MainViewModel
from desktop_client.presentation.services.dialog_service import DialogService
from desktop_client.services.telemetry_manager import TelemetryManager
from desktop_client.application.config_validator_service import ConfigValidatorService
from desktop_client.application.config_state_manager import ConfigStateManager
from desktop_client.presentation.viewmodels.config_viewmodel import ConfigViewModel
from desktop_client.domain.tuning import TuningSetup
from desktop_client.infrastructure.local_config_repository import LocalConfigRepository
from config import get_settings, BASE_DIR

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Sets up the environment for the application."""
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

async def async_main():
    """
    Async main entry point for the application.
    Bootstraps the QApplication and the main window with MVVM dependencies.
    Runs inside the unified qasync Qt+asyncio event loop.
    """
    # 1. Load Configuration
    try:
        settings = get_settings()
        logger.info(f"Configuration loaded successfully. Environment: {settings.env}")
    except Exception as e:
        logger.critical(f"Failed to load configuration: {e}")
        sys.exit(1)


    # 3. Initialize Dependencies (Services)
    logger.info("Initializing services...")
    telemetry_manager = TelemetryManager(api_url=settings.network.api_url)

    # 4. Initialize ViewModels
    logger.info("Initializing ViewModels...")
    main_vm = MainViewModel(telemetry_manager)
    
    app_config_validator = ConfigValidatorService(TuningSetup)
    local_config_repo = LocalConfigRepository(BASE_DIR)
    app_config_state_manager = ConfigStateManager(local_config_repo)
    app_config_state_manager.initialize(TuningSetup.model_validate)
    config_vm = ConfigViewModel(app_config_validator, app_config_state_manager)

    # 5. Initialize Dialog Services and View (Window)
    logger.info("Initializing View...")
    dialog_service = DialogService(main_vm, config_vm)
    window = MainWindow(main_vm, dialog_service)
    dialog_service.set_main_window(window)
    window.show()

    # 6. Wait for the Qt application to exit.
    # asyncio.get_event_loop().run_forever() is managed by QEventLoop below.
    # We use a Future to keep the coroutine alive until the app quits.
    future = asyncio.get_event_loop().create_future()

    def on_app_quit():
        if not future.done():
            future.set_result(None)

    QApplication.instance().aboutToQuit.connect(on_app_quit)
    await future


def main():
    """
    Synchronous entry point.
    Creates QApplication and installs the qasync event loop to unify
    Qt's and asyncio's event loops into a single cooperative loop.
    """
    setup_environment()

    app = QApplication(sys.argv)
    app.setApplicationName("ForzaAITuner")
    app.setApplicationVersion("1.0.0")

    # Install qasync event loop — this is the critical bridge between Qt and asyncio.
    # From this point on asyncio.get_event_loop() returns the Qt-managed event loop.
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