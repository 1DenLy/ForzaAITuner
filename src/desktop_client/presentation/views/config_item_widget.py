from typing import Any
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Slot

from desktop_client.presentation.ui.generated.ui_list_widget import Ui_ListWidget


class ConfigItemWidget(QWidget):
    """
    Custom widget for a single item in the library list.
    Dumb View: handles only appearance and user action forwarding.
    """
    edit_requested = Signal(str)
    delete_requested = Signal(str)
    export_requested = Signal(str)

    def __init__(self, config_data: dict[str, Any], parent=None):
        super().__init__(parent)
        self.ui = Ui_ListWidget()
        self.ui.setupUi(self)

        self._config_data = config_data
        self._config_id = str(config_data.get("id", ""))

        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Fill labels with data."""
        # TODO: Implement actual data mapping when UI labels are finalized
        pass

    def _setup_connections(self):
        # TODO: Connect buttons when they are available in UI
        pass

    @Slot()
    def _on_edit_clicked(self):
        self.edit_requested.emit(self._config_id)

    @Slot()
    def _on_delete_clicked(self):
        self.delete_requested.emit(self._config_id)