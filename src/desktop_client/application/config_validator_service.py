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

from pydantic import BaseModel, ValidationError

from desktop_client.application.validation_result import ValidationResult

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
                • is_valid=False, errors={loc: msg, ...} — если есть ошибки валидации.

        Raises:
            TypeError: Если raw_data не является dict (ошибка контракта).

        Note — strict mode:
            Pydantic по умолчанию делает мягкое приведение типов (Coercion):
            например, строка ``"12.5"`` станет ``float(12.5)`` автоматически.
            Для десктопного UI текущего поведения (мягкого) достаточно.
            Если raw_data придёт из недоверенного источника (сеть, API),
            замени model_validate на:
                ``self._model_class.model_validate(raw_data, strict=True)``
        """
        if not isinstance(raw_data, dict):
            raise TypeError(
                f"raw_data must be a dict, got {type(raw_data).__name__!r}. "
                "This is a caller contract error, not a user data validation error."
            )

        try:
            valid_model = self._model_class.model_validate(raw_data)
            return ValidationResult.success(valid_model)

        except ValidationError as exc:
            errors = self._parse_validation_errors(exc)
            return ValidationResult.failure(errors)

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_validation_errors(exc: ValidationError) -> dict[str, str]:
        """
        Преобразует pydantic.ValidationError в безопасный для UI словарь ошибок.

        Ключ:   строковый путь до поля внутри JSON, например ``"gearing -> gears -> 0"``.
        Значение: читаемая суть нарушения (msg) без stack-trace и системных путей —
                безопасно отображается в UI.

        i18n NOTE:
            Pydantic генерирует ``msg`` на английском
            (например: ``"Input should be greater than 0"`` для ``gt=0``).
            Для локализации (i18n) в будущем — мапить по ключу ``error.get("type")``:
                ``"greater_than"``, ``"missing"``, ``"string_type"`` и т.п.
            Таблица всех type-кодов:
            https://docs.pydantic.dev/latest/errors/validation_errors/

        Args:
            exc: Исключение pydantic.ValidationError.

        Returns:
            dict[str, str]: {field_loc_path: human_readable_message}.
        """
        errors: dict[str, str] = {}

        for error in exc.errors(include_url=False):
            loc_parts: tuple = error.get("loc", ())
            # Собираем путь только из "человеческих" сегментов (str | int),
            # исключая служебные вставки pydantic (function-before и т.п.)
            readable_parts = [str(part) for part in loc_parts]
            loc_key = " -> ".join(readable_parts) if readable_parts else "__root__"

            # Берём только msg — без url, ctx с внутренними деталями и input.
            # Для i18n: заменить msg на перевод из словаря
            # {error.get("type"): "Локализованное сообщение"}.
            msg: str = error.get("msg", "Invalid value")

            # Если под одним loc уже есть ошибка — дополняем через "; "
            if loc_key in errors:
                errors[loc_key] += f"; {msg}"
            else:
                errors[loc_key] = msg

        return errors
