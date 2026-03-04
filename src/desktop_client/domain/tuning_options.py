# -*- coding: utf-8 -*-
"""
Допустимые значения для ComboBox-полей конфигурации тюнинга.

Размещены в доменном слое — это бизнес-знание о том, какие
варианты существуют в игре, а не деталь UI или инфраструктуры.

Использование:
    from desktop_client.domain.tuning_options import TuningOptions
    TuningOptions.ROAD_TYPES          # ["Road", "Dirt", "Cross Country"]
    TuningOptions.for_path(("session", "road_type"))  # то же самое
"""

from __future__ import annotations


class TuningOptions:
    """
    Словарь допустимых значений для каждого str-поля модели.

    Ключ = model_path в виде tuple — совпадает с WidgetBinding.model_path,
    что позволяет маперу подставлять нужные списки автоматически.
    """

    # ── Session ───────────────────────────────────────────────────────────────
    ROAD_TYPES: list[str] = ["Road", "Dirt", "Cross Country"]

    LOCATIONS: list[str] = [
        "Open Horizon World",
        "Race against opponents",
        "Time Trial",
    ]

    SURFACES: list[str] = ["Dry", "Wet", "Snow / Ice"]

    # ── Car Info ──────────────────────────────────────────────────────────────
    DRIVE_TYPES: list[str] = ["AWD", "RWD", "FWD"]

    ENGINE_PLACEMENTS: list[str] = ["Front", "Mid", "Rear"]

    # ── Tires ─────────────────────────────────────────────────────────────────
    TIRE_COMPOUNDS: list[str] = [
        "Street",
        "Sport",
        "Semi-Slick",
        "Slick",
        "Rally",
        "Off-Road",
        "Mud",
        "Snow",
    ]

    # ── Assists ───────────────────────────────────────────────────────────────
    # Булевы поля хранятся как str("True"/"False") в комбобоксе
    BOOL_OPTIONS: list[str] = ["True", "False"]

    SHIFTING_OPTIONS: list[str] = ["Manual", "Manual w/ Clutch", "Automatic"]

    STEERING_OPTIONS: list[str] = ["Normal", "Simulation"]

    # ── Маппинг model_path → список значений ─────────────────────────────────
    _OPTIONS_MAP: dict[tuple[str, ...], list[str]] = {}

    @classmethod
    def _build_map(cls) -> dict[tuple[str, ...], list[str]]:
        return {
            ("session", "road_type"):        cls.ROAD_TYPES,
            ("session", "location"):         cls.LOCATIONS,
            ("session", "surface"):          cls.SURFACES,
            ("info", "drive_type"):          cls.DRIVE_TYPES,
            ("info", "engine_placement"):    cls.ENGINE_PLACEMENTS,
            ("tires", "compound"):           cls.TIRE_COMPOUNDS,
            ("assists", "abs"):              cls.BOOL_OPTIONS,
            ("assists", "stm"):              cls.BOOL_OPTIONS,
            ("assists", "tcs"):              cls.BOOL_OPTIONS,
            ("assists", "shifting"):         cls.SHIFTING_OPTIONS,
            ("assists", "steering"):         cls.STEERING_OPTIONS,
        }

    @classmethod
    def for_path(cls, model_path: tuple[str, ...]) -> list[str] | None:
        """
        Возвращает список допустимых значений по пути модели.

        Пример:
            TuningOptions.for_path(("session", "road_type"))
            # → ["Road", "Dirt", "Cross Country"]

            TuningOptions.for_path(("tires", "front_pressure_bar"))
            # → None  (не комбобокс)
        """
        if not cls._OPTIONS_MAP:
            cls._OPTIONS_MAP = cls._build_map()
        return cls._OPTIONS_MAP.get(model_path)
