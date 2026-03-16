from PySide6.QtCore import QObject, Signal, Slot
from typing import Optional
from desktop_client.domain.interface.i_config_data import IConfigData
from desktop_client.domain.interface.i_local_data import ILocalData
from desktop_client.application.state import LibraryFlowManager


class ConfigLibraryViewModel(QObject):

    list_updated = Signal(list)  
    error_occurred = Signal(str)

    def __init__(self, config_repo: IConfigData, local_state: ILocalData, library_flow: LibraryFlowManager):
        super().__init__()
        self._config_repo = config_repo
        self._local_state = local_state
        self._library_flow = library_flow

    @property
    def library_flow(self) -> LibraryFlowManager:
        return self._library_flow

    @Slot()
    def on_back_to_main_clicked(self):
        """Handle 'Back to Main' button click."""
        pass

    @Slot()
    def on_new_config_clicked(self):
        """Handle 'New config' button click."""
        pass

    @Slot(bool)
    def on_drive_type_awd_toggled(self, checked: bool):
        """Handle AWD filter checkbox."""
        pass

    @Slot(bool)
    def on_drive_type_rwd_toggled(self, checked: bool):
        """Handle RWD filter checkbox."""
        pass

    @Slot(bool)
    def on_drive_type_fwd_toggled(self, checked: bool):
        """Handle FWD filter checkbox."""
        pass
