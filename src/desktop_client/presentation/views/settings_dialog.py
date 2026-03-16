from PySide6.QtWidgets import QDialog, QDialogButtonBox
from PySide6.QtCore import Slot

from desktop_client.presentation.viewmodels.main_vm import MainViewModel
from desktop_client.presentation.ui.generated.ui_settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog):
    """
    Settings Dialog.
    Dumb View: No business logic, only setupUi and signal forwarding.
    """

    def __init__(self, viewmodel: MainViewModel, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self._vm = viewmodel
        self._setup_connections()

    def _setup_connections(self):
        # Override default accepted signal if needed, otherwise it's wired in setupUi
        # to accept(). If we need to perform logic in VM before accepting:
        try:
            self.ui.buttonBox.accepted.disconnect()
        except (RuntimeError, AttributeError):
            pass
        self.ui.buttonBox.accepted.connect(self._on_accepted)
        
        reset_btn = self.ui.buttonBox.button(QDialogButtonBox.Reset)
        if reset_btn:
            reset_btn.clicked.connect(self._on_reset_clicked)

    @Slot()
    def _on_accepted(self):
        """Forward save action to ViewModel."""
        # self._vm.save_settings(...)
        self.accept()

    @Slot()
    def _on_reset_clicked(self):
        """Forward reset action to ViewModel."""
        # self._vm.reset_settings()
        pass
