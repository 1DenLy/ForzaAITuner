"""
Конфигурационный ViewModel.
Связывает слой Application (ConfigValidatorService, ConfigStateManager) с UI (View).
Отвечает за конвертацию плоских словарей формы во вложенную структуру и маппинг ошибок.
"""

from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, Signal
from pydantic import ValidationError

from desktop_client.application.config_state_manager import ConfigStateManager
from desktop_client.application.config_validator_service import ConfigValidatorService
from desktop_client.application.exceptions import ConfigLockedError
from desktop_client.domain.tuning import TuningSetup
from desktop_client.domain.tuning_defaults import TuningDefaults
from desktop_client.presentation.services.security_utils import SecurityUtils
from config import BASE_DIR


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
        state_manager: ConfigStateManager,
        parent: QObject | None = None
    ) -> None:
        """
        Инициализирует ViewModel.
        
        Args:
            validator: Сервис валидации сырых данных в модели
            state_manager: Менеджер состояния для хранения конфигурации
            parent: Родительский QObject
        """
        super().__init__(parent)
        self._validator = validator
        self._state_manager = state_manager

    # ------------------------------------------------------------------ #
    # Public Methods                                                     #
    # ------------------------------------------------------------------ #

    def get_initial_data(self) -> dict[str, Any]:
        """
        Возвращает чистый словарь модели из state_manager для маппера.
        Если конфигурация ещё не загружена — возвращает доменные дефолты,
        чтобы форма открылась заполненной, а не пустой.
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
        result = self._validator.validate(raw_data_dict)
        
        if not result.is_valid:
            field_errors, global_errors = self._format_pydantic_errors(result.errors)
            self.validation_failed.emit(field_errors, global_errors)
            return

        try:
            self._state_manager.update_config(result.data)
            self.config_saved.emit()
        except ConfigLockedError as e:
            self.global_error_occurred.emit(str(e))

    def load_config_from_file(self, filepath: str) -> None:
        """
        Загружает пресет из файла, валидируя его схему Pydantic.
        Если схема верна, пробрасывает сырые данные дальше во View.
        """
        try:
            # 1. Security Validation: Path Traversal & DoS (File size)
            safe_path = SecurityUtils.validate_safe_path(filepath, BASE_DIR)
            SecurityUtils.validate_file_size(safe_path)

            # 2. Reading and Parsing
            text = safe_path.read_text(encoding="utf-8")
            config = TuningSetup.model_validate_json(text)
            self.preset_loaded.emit(config.model_dump(mode="json"))
        except ValidationError as e:
            # Для ошибок структуры файла при парсинге (Pydantic ValidationError наследуется от ValueError, 
            # поэтому этот блок должен идти ПЕРВЫМ)
            self.global_error_occurred.emit(f"Ошибка содержимого файла пресета:\n{str(e)}")
        except (PermissionError, ValueError) as e:
            # Security violations (Traversal or oversized file)
            self.global_error_occurred.emit(f"Ошибка безопасности:\n{str(e)}")
        except Exception as e:
            self.global_error_occurred.emit(f"Ошибка чтения файла:\n{str(e)}")

    def _format_pydantic_errors(self, pydantic_errors: dict[str, str]) -> tuple[dict[str, str], list[str]]:
        """
        Разделяет ошибки от ConfigValidatorService на field_errors и global_errors.
        Пути с сепаратором ' -> ' форматируются в точечную нотацию. 
        """
        field_errors = {}
        global_errors = []
        for loc_key, msg in pydantic_errors.items():
            if loc_key == "__root__" or loc_key == "":
                global_errors.append(msg)
            else:
                dot_key = loc_key.replace(" -> ", ".")
                field_errors[dot_key] = msg
        return field_errors, global_errors
