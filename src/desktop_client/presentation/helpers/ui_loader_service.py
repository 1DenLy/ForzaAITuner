from pathlib import Path
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject

from desktop_client.presentation.helpers.security_utils import SecurityUtils


class UiLoaderService:
    """
    Service for securely loading .ui files.

    Single Responsibility — only handles Qt UI file loading.
    Path safety is delegated to SecurityUtils.validate_safe_path.
    """

    @staticmethod
    def load_ui(ui_file_path: str, parent: QObject = None) -> QObject:
        """
        Loads a .ui file safely.

        Args:
            ui_file_path (str): The absolute path to the .ui file.
            parent (QObject, optional): Parent object for the loaded UI.

        Returns:
            QObject: The loaded UI widget/window.

        Raises:
            PermissionError:    If a path-traversal attempt is detected.
            FileNotFoundError:  If the file does not exist.
            ValueError:         If the file is not a .ui file, or exceeds the
                                maximum allowed size (see SecurityUtils.MAX_UI_FILE_BYTES).
            RuntimeError:       If Qt loading fails.
        """
        from config import BASE_DIR  # imported late to avoid circular imports

        # 1. Security & validation — delegated to SecurityUtils (SRP)
        ui_path_obj = SecurityUtils.validate_safe_path(ui_file_path, BASE_DIR)

        if not ui_path_obj.exists():
            raise FileNotFoundError(f"UI file not found: {ui_file_path}")

        if ui_path_obj.suffix.lower() != ".ui":
            raise ValueError(f"Invalid file extension. Expected .ui file: {ui_file_path}")

        # Guard against XML-bomb / OOM: reject oversized files before Qt touches them
        SecurityUtils.validate_file_size(ui_path_obj)

        # 2. Qt loading
        loader = QUiLoader()
        ui_file = QFile(str(ui_path_obj))

        if not ui_file.open(QIODevice.ReadOnly):
            raise RuntimeError(f"Cannot open {ui_file_path}: {ui_file.errorString()}")

        try:
            loaded_widget = loader.load(ui_file, parent)
        finally:
            ui_file.close()

        if not loaded_widget:
            raise RuntimeError(f"Loader failed to load {ui_file_path}")

        return loaded_widget
