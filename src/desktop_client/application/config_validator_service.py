"""
ConfigValidatorService — Generic слой Application/Use Cases.

Ответственность: ТОЛЬКО парсинг и валидация сырых словарей (raw_data: dict)
в строго типизированные Pydantic-модели. Никакой работы с файлами,
путями или json.load() — это зона Infrastructure (Step 2).

Соответствие DIP: сервис Generic, не привязан к конкретной конфигурационной модели.
Caller сам указывает целевой тип через target_model: Type[TModel].

Обработка исключений (Anti-Pokemon):
  • Перехватывается строго pydantic.ValidationError.
  • Любой TypeError (например, передан список вместо dict) пробрасывается выше —
    это ошибка контракта вызывающего кода, а не пользовательских данных.
"""

from __future__ import annotations

from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel, ValidationError as PydanticValidationError

from desktop_client.validation.models import (
    ValidationResult, 
    ValidationError, 
    ValidationErrorCode
)

TModel = TypeVar("TModel", bound=BaseModel)


class ConfigValidatorService(Generic[TModel]):
    """
    Generic-сервис валидации конфигурации.

    Принимает любой Pydantic BaseModel-подкласс и умеет валидировать
    произвольные сырые словари в экземпляр этой модели.

    Пример использования::

        from desktop_client.domain.tuning import TuningSetup

        validator = ConfigValidatorService(TuningSetup)
        result = validator.validate(raw_data)

        if result.is_valid:
            setup: TuningSetup = result.data
        else:
            for field_path, message in result.errors.items():
                print(f"{field_path}: {message}")
    """

    def __init__(self, target_model: Type[TModel]) -> None:
        """
        Args:
            target_model: Pydantic-модель, в которую будут валидироваться сырые данные.
        """
        self._model_class = target_model

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def validate(self, raw_data: dict[str, Any]) -> ValidationResult[TModel]:
        """
        Валидирует сырой словарь, возвращает ValidationResult.

        Args:
            raw_data: Сырой словарь данных (например, из UI или прочитанный репозиторием).
                      ДОЛЖЕН быть именно dict — передача других типов
                      (list, str и т.п.) вызовет TypeError, который пробрасывается выше.

        Returns:
            ValidationResult[TModel]:
                • is_valid=True, data=<экземпляр модели> — если данные корректны.
                • is_valid=False, errors=(ValidationError, ...) — если есть ошибки валидации.

        Raises:
            TypeError: Если raw_data не является dict (ошибка контракта).
        """
        if not isinstance(raw_data, dict):
            raise TypeError(
                f"raw_data must be a dict, got {type(raw_data).__name__!r}. "
                "This is a caller contract error, not a user data validation error."
            )

        try:
            valid_model = self._model_class.model_validate(raw_data)
            return ValidationResult(is_valid=True, data=valid_model)

        except PydanticValidationError as exc:
            errors = self._parse_validation_errors(exc)
            return ValidationResult(is_valid=False, errors=errors)

    def validate_json(self, json_text: str) -> ValidationResult[TModel]:
        """
        Валидирует JSON-строку, возвращает ValidationResult.
        """
        try:
            valid_model = self._model_class.model_validate_json(json_text)
            return ValidationResult(is_valid=True, data=valid_model)
        except PydanticValidationError as exc:
            errors = self._parse_validation_errors(exc)
            return ValidationResult(is_valid=False, errors=errors)

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_validation_errors(exc: PydanticValidationError) -> tuple[ValidationError, ...]:
        """
        Преобразует pydantic.ValidationError в стандартизированный список ValidationError.
        """
        errors: list[ValidationError] = []

        for error in exc.errors(include_url=False):
            loc_parts: tuple = error.get("loc", ())
            readable_parts = [str(part) for part in loc_parts]
            # Используем dot-notation по умолчанию для совместимости с UI
            loc_key = ".".join(readable_parts) if readable_parts else None

            msg: str = error.get("msg", "Invalid value")

            errors.append(ValidationError(
                code=ValidationErrorCode.SCHEMA_ERROR,
                message=msg,
                location=loc_key
            ))

        return tuple(errors)
