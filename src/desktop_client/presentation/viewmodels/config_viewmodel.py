"""
Конфигурационный ViewModel.
Связывает слой Application (ConfigValidatorService, ConfigStateManager) с UI (View).
Отвечает за конвертацию плоских словарей формы во вложенную структуру и маппинг ошибок.
"""

from typing import Any

from PySide6.QtCore import QObject, Signal

from desktop_client.application.config_state_manager import ConfigStateManager
from desktop_client.application.config_validator_service import ConfigValidatorService
from desktop_client.application.exceptions import ConfigLockedError
from desktop_client.domain.tuning_defaults import TuningDefaults


class ConfigViewModel(QObject):
    """
    ViewModel для диалога конфигурации.
    Поддерживает бизнес-логику работы с плоскими формами UI.
    """

    # --- Сигналы ---
    # Передает словарь ошибок вида {"tires.front_pressure_bar": "Ошибка..."}
    validation_failed = Signal(dict)
    
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
            formatted_errors = self._format_pydantic_errors(result.errors)
            self.validation_failed.emit(formatted_errors)
            return

        try:
            self._state_manager.update_config(result.data)
            self.config_saved.emit()
        except ConfigLockedError as e:
            self.global_error_occurred.emit(str(e))

    def _format_pydantic_errors(self, pydantic_errors: dict[str, str]) -> dict[str, str]:
        """
        Преобразует пути ошибок от ConfigValidatorService (с ' -> ' сепаратором) в точечную нотацию.
        """
        formatted = {}
        for loc_key, msg in pydantic_errors.items():
            dot_key = loc_key.replace(" -> ", ".")
            formatted[dot_key] = msg
        return formatted
