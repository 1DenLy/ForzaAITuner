"""
ValidationResult — Generic Result-паттерн для слоя Application/Use Cases.

Обеспечивает единый формат ответа от сервиса валидации.
Вызывающий код (ViewModel) всегда получает этот объект вместо исключений.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

# Bound to pydantic BaseModel to preserve type-safety at call-site.
T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ValidationResult(Generic[T]):
    """
    Иммутабельный контейнер результата валидации.

    Attributes:
        is_valid: True — данные прошли валидацию, ``data`` заполнен.
                  False — есть ошибки, ``errors`` заполнен.
        errors:   Словарь {loc_path: message}.
                  ``loc_path`` — строковый путь до поля внутри JSON
                  (например ``"gearing -> gears -> 0"``).
                  Значения содержат только суть нарушения без stack-trace —
                  безопасны для отображения в UI.
        data:     Готовый доменный объект. Заполняется ТОЛЬКО если is_valid == True.

    Pattern Matching (Python 3.10+):
        ``@dataclass(slots=True)`` автоматически генерирует ``__match_args__``
        из порядка объявленных полей: ``('is_valid', 'errors', 'data')``.
        Это делает работу ключевых паттернов полностью прозрачной во ViewModel::

            match validator.validate(raw):
                case ValidationResult(is_valid=True, data=cfg):
                    self._apply_config(cfg)
                case ValidationResult(is_valid=False, errors=errs):
                    self._show_errors(errs)

        Важно: НЕ объявляем ``__match_args__`` вручную — при ``slots=True``
        dataclass уже выставляет его сам, повторное объявление вызовет ValueError.
    """

    is_valid: bool
    errors: dict[str, str] = field(default_factory=dict)
    data: Optional[T] = None

    # ------------------------------------------------------------------ #
    # Фабричные методы                                                     #
    # ------------------------------------------------------------------ #

    @classmethod
    def success(cls, data: T) -> "ValidationResult[T]":
        """Создаёт результат успешной валидации."""
        return cls(is_valid=True, errors={}, data=data)

    @classmethod
    def failure(cls, errors: dict[str, str]) -> "ValidationResult[T]":
        """Создаёт результат неуспешной валидации с картой ошибок."""
        return cls(is_valid=False, errors=errors, data=None)
