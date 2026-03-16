"""
Конфигурационный ViewModel.
Связывает слой Application (ConfigValidatorService, ConfigDataManager) с UI (View).
Отвечает за конвертацию плоских словарей формы во вложенную структуру и маппинг ошибок.
"""

import logging
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, Signal

from desktop_client.application.config_data_manager import ConfigDataManager
from desktop_client.application.config_validator_service import ConfigValidatorService
from desktop_client.application.exceptions import ConfigLockedError, PresetLoadError
from desktop_client.application.state import ConfigFlowManager
from desktop_client.domain.tuning_defaults import TuningDefaults
from desktop_client.domain.models import ConfigState
from desktop_client.presentation.interfaces.protocols import IPresetRepository
from desktop_client.presentation.resources.strings import UIStrings
from desktop_client.validation.ui_formatter import format_errors_for_ui

_logger = logging.getLogger(__name__)


class ConfigViewModel(QObject):
    """
    ViewModel для диалога конфигурации.
    Поддерживает бизнес-логику работы с плоскими формами UI.
    """

    # --- Сигналы ---
    # Передает словарь field_errors и список global_errors
    validation_failed = Signal(dict, list)
    
    # Сигнал загрузки пресета в форму
    preset_loaded = Signal(dict)
    
    # Сигнал успешного сохранения
    config_saved = Signal()
    
    # Сигнал для критических ошибок (например, блокировка конфига)
    global_error_occurred = Signal(str)

    def __init__(
        self,
        validator: ConfigValidatorService,
        state_manager: ConfigDataManager,
        preset_repository: IPresetRepository,
        config_flow: ConfigFlowManager,
        parent: QObject | None = None
    ) -> None:
        """
        Инициализирует ViewModel.
        
        Args:
            validator: Сервис валидации сырых данных в модели
            state_manager: Менеджер состояния для хранения конфигурации
            preset_repository: Репозиторий для загрузки пресетов
            parent: Родительский QObject
        """
        super().__init__(parent)
        self._validator = validator
        self._state_manager = state_manager
        self._preset_repository = preset_repository
        self._config_flow = config_flow

    @property
    def config_flow(self) -> ConfigFlowManager:
        return self._config_flow

    # ------------------------------------------------------------------ #
    # Public Methods                                                     #
    # ------------------------------------------------------------------ #

    def get_last_valid_config(self) -> dict[str, Any]:
        """
        Возвращает чистый словарь модели (TuningSetup) из state_manager.
        Это 'последнее валидное сохраненное состояние'.
        Если конфигурация ещё не загружена — возвращает доменные дефолты.
        """
        config = self._state_manager.get_config()
        if config is not None:
            return config.model_dump(mode="json")
        return TuningDefaults.as_dict()

    def apply_config(self, raw_data_dict: dict[str, Any]) -> None:
        """
        Обрабатывает событие сохранения формы от View.
        Здесь raw_data_dict уже имеет правильную вложенную структуру благодаря мапперу.
        """
        self._config_flow.set_state(ConfigState.VALIDATING)
        result = self._validator.validate(raw_data_dict)
        
        if not result.is_valid:
            self._config_flow.set_state(ConfigState.INVALID)
            field_errors, global_errors = format_errors_for_ui(result)
            self.validation_failed.emit(field_errors, global_errors)
            return

        try:
            self._config_flow.set_state(ConfigState.SAVING)
            self._state_manager.update_config(result.data)
            self._config_flow.set_state(ConfigState.READY)
            self.config_saved.emit()
        except ConfigLockedError as e:
            self._config_flow.set_state(ConfigState.EDITING)
            self.global_error_occurred.emit(str(e))

    def load_config_from_file(self, filepath: str) -> None:
        """
        Загружает пресет из файла, валидируя его схему.
        Если схема верна, пробрасывает сырые данные дальше во View.
        """
        try:
            # Reading is delegated to the repository
            text = self._preset_repository.load_preset(filepath)
            result = self._validator.validate_json(text)
            
            if result.is_valid and result.data is not None:
                self.preset_loaded.emit(result.data.model_dump(mode="json"))
            else:
                # Format specific errors if possible, or just show a general error
                _, global_errors = format_errors_for_ui(result)
                err_msg = ", ".join(global_errors) if global_errors else "Validation failed"
                _logger.warning(f"Validation failed for preset {filepath}: {err_msg}")
                self.global_error_occurred.emit(UIStrings.ERR_PRESET_SCHEMA.format(err_msg))
                
        except PresetLoadError as e:
            # Domain exception from repository (wraps OS and security errors)
            _logger.error(f"Failed to load preset {filepath}", exc_info=True)
            self.global_error_occurred.emit(UIStrings.ERR_LOAD_PRESET)
        except ValueError as e:
            # Likely JSON decoding error from validate_json or similar
            _logger.error(f"Invalid JSON in preset {filepath}", exc_info=True)
            self.global_error_occurred.emit(UIStrings.ERR_INVALID_JSON_FORMAT.format(str(e)))
        except Exception as e:
            # Catch-all for unexpected bugs
            _logger.critical(f"Unexpected error while loading preset {filepath}", exc_info=True)
            self.global_error_occurred.emit(UIStrings.ERR_GENERIC.format("Unexpected error"))

