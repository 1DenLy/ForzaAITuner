# -*- coding: utf-8 -*-
"""Функции трансформации данных между UI (int) и моделью (float)."""

from __future__ import annotations

import logging
import math
from typing import Callable

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Фабрики (приватные)
# ---------------------------------------------------------------------------

def _make_to_model(factor: float) -> Callable[[int | float], float]:
    """Делит сырое UI-значение на ``factor``. При ошибке возвращает ``0.0``."""
    if factor <= 0:
        raise ValueError(f"factor must be > 0, got {factor!r}")

    precision = max(0, math.ceil(math.log10(factor))) if factor > 1 else 0

    def to_model(raw: int | float) -> float:
        try:
            return round(float(raw) / factor, precision)
        except (TypeError, ValueError) as exc:
            logger.warning("to_model_x%s: bad input %r — returning 0.0 (%s)", factor, raw, exc)
            return 0.0

    to_model.__name__ = f"to_model_x{factor}"
    return to_model


def _make_to_ui(factor: float) -> Callable[[float], int]:
    """Умножает значение модели на ``factor`` и приводит к int. При ошибке возвращает ``0``."""
    if factor <= 0:
        raise ValueError(f"factor must be > 0, got {factor!r}")

    def to_ui(value: float) -> int:
        try:
            return int(round(float(value) * factor))
        except (TypeError, ValueError) as exc:
            logger.warning("to_ui_x%s: bad input %r — returning 0 (%s)", factor, value, exc)
            return 0

    to_ui.__name__ = f"to_ui_x{factor}"
    return to_ui


def _make_pair(factor: float) -> tuple[Callable[[int | float], float], Callable[[float], int]]:
    """Возвращает пару ``(to_model, to_ui)`` для заданного масштаба."""
    return _make_to_model(factor), _make_to_ui(factor)


# ---------------------------------------------------------------------------
# Публичные функции
# ---------------------------------------------------------------------------

# ×10 — шаг 0.1: слайдер 21 → модель 2.1
slider_x10_to_model, slider_x10_to_ui = _make_pair(10)

# ×1  — шаг 1.0: слайдер 65 → модель 65.0
slider_x1_to_model, slider_x1_to_ui = _make_pair(1)


def str_to_bool(raw: str) -> bool:
    """``"True"`` → ``True``, всё остальное → ``False``."""
    return str(raw).lower() == "true"


def bool_to_str(value: bool) -> str:
    """``True`` → ``"True"``, ``False`` → ``"False"``."""
    return "True" if value else "False"
