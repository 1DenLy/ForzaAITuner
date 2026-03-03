from PySide6.QtCore import QObject
from PySide6.QtWidgets import QDialog
from desktop_client.presentation.services.ui_loader_service import UiLoaderService

class BaseDialog(QObject):
    """
    Base dialog class that manages UI loading via UiLoaderService.
    Encapsulates the loaded UI QDialog widget.
    """
    def __init__(self, ui_file_path: str, parent=None):
        super().__init__(parent)
        # Load the UI content
        self._ui_widget: QDialog = UiLoaderService.load_ui(ui_file_path, parent)
        
    @property
    def ui(self) -> QDialog:
        """Access the raw loaded UI object."""
        return self._ui_widget

    def exec(self):
        """Shows the dialog as a modal window."""
        if self._ui_widget:
            return self._ui_widget.exec()
        return QDialog.DialogCode.Rejected
