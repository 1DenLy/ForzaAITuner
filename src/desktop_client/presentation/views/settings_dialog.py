from PySide6.QtWidgets import QDialog

from desktop_client.presentation.interfaces.protocols import IMainViewModel
from desktop_client.presentation.ui.generated.ui_settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog):
    """
    Settings Dialog.

    AOT approach: uses pyside6-uic–generated Ui_SettingsDialog for fast,
    type-safe UI setup (no runtime QUiLoader).
    """

    def __init__(self, view_model: IMainViewModel, parent=None):
        super().__init__(parent)
        self._vm = view_model

        # Setup AOT-compiled UI
        self._ui = Ui_SettingsDialog()
        self._ui.setupUi(self)

        # buttonBox accepted/rejected are already wired to accept()/reject()
        # in the generated setupUi.
        self.accepted.connect(self._on_accepted)

    def _on_accepted(self):
        """Called when the user confirms the dialog (OK button)."""
        # TODO: apply settings to the appropriate service/model
        pass
