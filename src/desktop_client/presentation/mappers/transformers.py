# -*- coding: utf-8 -*-
"""
Чистые функции трансформации данных между UI (int) и моделью (float).

Вынесены из _init_bindings в TuningMapper, чтобы:
  - их можно было тестировать изолированно (unit-тесты без Qt);
  - нейминг отражал намерение, а не реализацию (scale_x10 / scale_x1);
  - лямбды не захламляли пространство имён метода.

Все методы — статические, без состояния, чистые (pure functions).
"""

from __future__ import annotations


class Transformers:
    """Пространство имён для функций трансформации виджет↔модель."""

    # ── Слайдеры с ценой деления 0.1 (×10) ─────────────────────────────────

    @staticmethod
    def slider_x10_to_model(raw: int | float) -> float:
        """Слайдер (целое) → модель: делим на 10. Пример: 21 → 2.1."""
        return round(float(raw) / 10.0, 2)

    @staticmethod
    def slider_x10_to_ui(value: float) -> int:
        """Модель → слайдер: умножаем на 10. Пример: 2.1 → 21."""
        return int(float(value) * 10)

    # ── Слайдеры с ценой деления 1.0 (×1) ──────────────────────────────────

    @staticmethod
    def slider_x1_to_model(raw: int | float) -> float:
        """Слайдер (целое) → модель: приводим к float. Пример: 65 → 65.0."""
        return float(raw)

    @staticmethod
    def slider_x1_to_ui(value: float) -> int:
        """Модель → слайдер: обрезаем дробную часть. Пример: 65.0 → 65."""
        return int(float(value))

    # ── Булевы комбобоксы ("True" / "False") ────────────────────────────────

    @staticmethod
    def str_to_bool(raw: str) -> bool:
        """Строка из QComboBox → bool. Пример: "True" → True."""
        return str(raw).lower() == "true"

    @staticmethod
    def bool_to_str(value: bool) -> str:
        """Bool → строка для QComboBox. Пример: False → "False"."""
        return "True" if value else "False"
