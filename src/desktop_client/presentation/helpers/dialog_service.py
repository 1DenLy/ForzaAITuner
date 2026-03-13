from typing import Optional
from PySide6.QtWidgets import QWidget

from desktop_client.presentation.views.config_dialog import ConfigDialog
from desktop_client.presentation.views.settings_dialog import SettingsDialog
from desktop_client.presentation.interfaces.protocols import IDialogService, IMainViewModel, IConfigViewModel


class DialogService(IDialogService):
    """
    Concrete implementation of IDialogService.

    AOT-only: dialogs no longer receive a ui_path because they use
    pyside6-uic–generated classes internally.
    """

    def __init__(self, view_model: IMainViewModel, config_vm: IConfigViewModel):
        self._vm = view_model
        self._config_vm = config_vm
        self._main_window: Optional[QWidget] = None

    def set_main_window(self, window: QWidget) -> None:
        self._main_window = window

    def show_config_dialog(self) -> None:
        dialog = ConfigDialog(self._config_vm, self._main_window)
        dialog.exec()

    def show_settings_dialog(self) -> None:
        dialog = SettingsDialog(self._vm, self._main_window)
        dialog.exec()
