import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject

class UiLoaderService:
    """
    Service for securely loading .ui files.
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
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a .ui file or path is invalid.
            RuntimeError: If loading fails.
        """
        # 1. Path Validation & Security
        if not os.path.isabs(ui_file_path):
             # Force absolute path usage or assume relative to a known root if needed, 
             # but user instruction implies passing paths. Helper can enforce existence.
             ui_file_path = os.path.abspath(ui_file_path)

        if not os.path.exists(ui_file_path):
            raise FileNotFoundError(f"UI file not found: {ui_file_path}")
            
        if not ui_file_path.lower().endswith(".ui"):
            raise ValueError(f"Invalid file extension. Expected .ui file: {ui_file_path}")

        # Basic Path Traversal check: Ensure it's within the project directory? 
        # For now, we trust the caller provides a path, but we checked existence.
        
        # 2. Loading
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        
        if not ui_file.open(QIODevice.ReadOnly):
            raise RuntimeError(f"Cannot open {ui_file_path}: {ui_file.errorString()}")
        
        try:
            # Note: We pass parent if provided, but typically parent logic is handled by caller specific to layout
            loaded_widget = loader.load(ui_file, parent)
        finally:
            ui_file.close()

        if not loaded_widget:
             raise RuntimeError(f"Loader failed to load {ui_file_path}")
             
        return loaded_widget
