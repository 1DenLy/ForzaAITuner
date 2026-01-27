import sys
import logging
import signal
from pathlib import Path
from PySide6.QtWidgets import QApplication
from src.presentation.views.main_window import BaseWindow
from src.config import get_settings, BASE_DIR

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Sets up the environment for the application."""
    # Ensure project root is in sys.path
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

def handle_sigint(signum, frame):
    """Handles KeyboardInterrupt (Ctrl+C)."""
    logger.info("Received SIGINT (Ctrl+C). Exiting...")
    QApplication.quit()

def main():
    """
    Main entry point for the application.
    Bootstraps the QApplication and the main window.
    """
    # Setup environment
    setup_environment()
    
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, handle_sigint)
    # Allow python to process signals periodically
    timer = None 

    try:
        # Load configuration (Fail-Safe check)
        try:
            settings = get_settings()
            logger.info(f"Configuration loaded successfully. Environment: {settings.env}")
        except Exception as e:
             logger.critical(f"Failed to load configuration: {e}")
             sys.exit(1)

        # Initialize the Application
        app = QApplication(sys.argv)
        app.setApplicationName("ForzaAITuner")
        app.setApplicationVersion("1.0.0") # You might want to pull this from config or pyproject.toml

        # Resolve UI path from settings
        # BASE_DIR is resolved in config.py securely
        ui_path = BASE_DIR / settings.ui.main_window_path

        logger.info(f"Starting application from: {BASE_DIR}")
        logger.info(f"Loading UI from: {ui_path}")

        if not ui_path.exists():
            logger.critical(f"UI file not found at: {ui_path}")
            sys.exit(1)

        # Initialize Main Window
        window = BaseWindow(str(ui_path))
        window.show()

        # Enable checking for Ctrl-C by using a timer to wake up the Qt event loop
        # This is a common workaround for PySide/PyQt to play nice with Python signals
        from PySide6.QtCore import QTimer
        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(500)

        # Execute Application
        sys.exit(app.exec())

    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()