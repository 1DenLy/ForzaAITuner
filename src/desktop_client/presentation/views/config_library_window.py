from PySide6.QtWidgets import QWidget, QMessageBox, QListView, QVBoxLayout
from PySide6.QtCore import Slot

from desktop_client.presentation.ui.generated.ui_config_library import Ui_ConfigLibrary
from desktop_client.presentation.viewmodels.config_library_viewmodel import ConfigLibraryViewModel
from desktop_client.presentation.views.config_list_model import ConfigListModel
from desktop_client.presentation.views.config_item_delegate import ConfigItemDelegate
from desktop_client.domain.models import LibraryState


class ConfigLibraryWindow(QWidget):
    """
    Config Library Window.
    Dumb View: No business logic, only setupUi, action forwarding, and signal reaction.
    """

    def __init__(self, viewmodel: ConfigLibraryViewModel, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConfigLibrary()
        self.ui.setupUi(self)

        self._vm = viewmodel
        
        # --- Model/View Setup (Phase 4 Optimization) ---
        self._list_model = ConfigListModel(self)
        self._list_delegate = ConfigItemDelegate(self)
        
        # Programmatically replace/augment the UI
        # We assume self.ui.listWidget exists and is in some layout
        self.ui.listWidget.setVisible(False)
        
        # If the parent has a layout, we can inject there.
        # Minimal: just use the model/view.
        # For simplicity, we create a new layout if none exists or reuse parent's.
        if self.ui.listWidget.parentWidget():
            parent = self.ui.listWidget.parentWidget()
            if parent.layout():
                # Replace listWidget in layout
                parent.layout().replaceWidget(self.ui.listWidget, self._create_list_view())
            else:
                layout = QVBoxLayout(parent)
                layout.addWidget(self._create_list_view())
        
        self._setup_connections()

        # Initial UI update
        self._on_state_changed(self._vm.library_flow.state)

    def _create_list_view(self) -> QListView:
        self.list_view = QListView()
        self.list_view.setModel(self._list_model)
        self.list_view.setItemDelegate(self._list_delegate)
        # Aesthetics
        self.list_view.setStyleSheet("background-color: transparent; border: none;")
        self.list_view.setSpacing(4)
        return self.list_view

    def _setup_connections(self):
        # View -> ViewModel
        self.ui.btn_back.clicked.connect(self._vm.on_back_to_main_clicked)
        self.ui.btn_new_config.clicked.connect(self._vm.on_new_config_clicked)

        # ViewModel -> View
        self._vm.list_updated.connect(self._populate_list)
        self._vm.error_occurred.connect(self._show_error)
        self._vm.library_flow.state_changed.connect(self._on_state_changed)

    @Slot(list)
    def _populate_list(self, configs: list):
        """Updates the model with new data."""
        self._list_model.set_configs(configs)

    @Slot(LibraryState)
    def _on_state_changed(self, state: LibraryState):
        """Update UI based on LibraryState Enum."""
        # Example: Disable "New Config" button if deleting
        self.ui.btn_new_config.setEnabled(state == LibraryState.VIEWING)
        self.ui.btn_back.setEnabled(state == LibraryState.VIEWING)

    @Slot(str)
    def _show_error(self, message: str):
        QMessageBox.critical(self, "Error", message)