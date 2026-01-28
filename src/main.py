import sys
import logging
import signal
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from src.presentation.views.main_window import MainWindow
from src.presentation.viewmodels.main_vm import MainViewModel
from src.presentation.services.config_validator import ConfigValidator
from src.forza_core.application.core_facade import RealCoreFacade
from src.config import get_settings, BASE_DIR

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Sets up the environment for the application."""
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

def handle_sigint(signum, frame):
    """Handles KeyboardInterrupt (Ctrl+C)."""
    logger.info("Received SIGINT (Ctrl+C). Exiting...")
    QApplication.quit()

def main():
    """
    Main entry point for the application.
    Bootstraps the QApplication and the main window with MVVM dependencies.
    """
    setup_environment()
    signal.signal(signal.SIGINT, handle_sigint)

    try:
        # 1. Load Configuration
        try:
            settings = get_settings()
            logger.info(f"Configuration loaded successfully. Environment: {settings.env}")
        except Exception as e:
            logger.critical(f"Failed to load configuration: {e}")
            sys.exit(1)

        # 2. Initialize Application
        app = QApplication(sys.argv)
        app.setApplicationName("ForzaAITuner")
        app.setApplicationVersion("1.0.0")

        # 3. Resolve Resources
        ui_path = BASE_DIR / settings.ui.main_window_path
        if not ui_path.exists():
            logger.critical(f"UI file not found at: {ui_path}")
            sys.exit(1)

        # 4. Initialize Dependencies (Services)
        logger.info("Initializing services...")
        core_facade = RealCoreFacade()
        config_validator = ConfigValidator()

        # 5. Initialize ViewModel
        logger.info("Initializing ViewModel...")
        main_vm = MainViewModel(core_facade, config_validator)

        # 6. Initialize View (Window)
        logger.info("Initializing View...")
        window = MainWindow(str(ui_path), main_vm)
        window.show()

        # 7. Setup Signal Handling Helper
        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(500)

        # 8. Execute
        sys.exit(app.exec())

    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()