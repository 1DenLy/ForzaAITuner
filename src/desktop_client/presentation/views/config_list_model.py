from typing import Any
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex


class ConfigListModel(QAbstractListModel):
    """
    Model for the list of configurations.
    More efficient than QListWidget for large datasets.
    """
    
    DATA_ROLE = Qt.UserRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._configs: list[dict[str, Any]] = []

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._configs)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid() or not (0 <= index.row() < len(self._configs)):
            return None

        config = self._configs[index.row()]

        if role == Qt.DisplayRole:
            # Basic fallback if no delegate is used
            return config.get("car_name", "Unknown Car")
        
        if role == self.DATA_ROLE:
            return config

        return None

    def set_configs(self, configs: list[dict[str, Any]]):
        """Updates the configuration list and notifies the view."""
        self.beginResetModel()
        self._configs = configs
        self.endResetModel()

    def get_config_at(self, row: int) -> dict[str, Any] | None:
        if 0 <= row < len(self._configs):
            return self._configs[row]
        return None
