# -*- coding: utf-8 -*-
"""
Дефолтные значения конфигурации тюнинга.

Размещены в доменном слое, потому что «разумные начальные значения» —
это бизнес-знание, а не деталь UI или инфраструктуры.

Использование:
    defaults = TuningDefaults.create()                                # TuningSetup с дефолтами
    raw_dict = TuningDefaults.as_dict()                               # dict для маппера/репозитория
    slider_default = TuningDefaults.get(("tires", "front_pressure_bar"))  # 2.0
    lo, hi = TuningDefaults.get_range(("tires", "front_pressure_bar"))    # (1.0, 3.8)
"""

from __future__ import annotations

from typing import Any

from desktop_client.domain.tuning import (
    Alignment,
    AntiRollBars,
    Aerodynamics,
    Assists,
    Brakes,
    CarInfo,
    Damping,
    Differential,
    Gearing,
    Session,
    Suspension,
    Tires,
    TuningSetup,
)


class TuningDefaults:
    """
    Фабрика дефолтных значений для TuningSetup.

    Все значения подобраны как «нейтральный» старт для настройки
    (середина разрешённого диапазона или типичный road-car baseline).
    """

    @classmethod
    def create(cls) -> TuningSetup:
        """Возвращает TuningSetup с разумными дефолтными значениями."""
        return TuningSetup(
            session=Session(
                name="",
                car="",
                class_pi=100,
                road_type="Road",
                location="Open Horizon World",
                surface="Dry",
            ),
            info=CarInfo(
                weight=1,             # gt=0: пользователь заполнит под свой автомобиль
                power=1,
                torque=1,
                front_weight=50.0,
                suspension_travel=1,
                drive_type="RWD",
                engine_placement="Front",
            ),
            tires=Tires(
                front_pressure_bar=2.0,
                rear_pressure_bar=2.0,
                width_front=1,    # gt=0: пользователь заполнит
                width_rear=1,
                compound="Sport",
            ),
            gearing=Gearing(
                final_drive=0.1,      # gt=0
                gears=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1],  # gt=0
            ),
            alignment=Alignment(
                camber_front_deg=-1.5,
                camber_rear_deg=-1.0,
                toe_front_deg=0.0,
                toe_rear_deg=0.0,
                caster_front_deg=5.0,
            ),
            anti_roll_bars=AntiRollBars(
                front=32.0,
                rear=28.0,
            ),
            suspension=Suspension(
                spring_front=0.1,      # gt=0: пользователь заполнит под автомобиль
                spring_rear=0.1,
                spring_min=0.1,
                spring_max=0.1,
                clearance_front=0.1,
                clearance_rear=0.1,
                clearance_min=0.1,
                clearance_max=0.1,
            ),
            damping=Damping(
                rebound_front=1.0,     # ge=1.0
                rebound_rear=1.0,
                rebound_min=1.0,
                rebound_max=1.0,
                bump_front=1.0,
                bump_rear=1.0,
                bump_min=1.0,
                bump_max=1.0,
            ),
            aerodynamics=Aerodynamics(
                front_enabled=False,
                rear_enabled=False,
                front=0.0,
                front_min=0.0,
                front_max=0.0,
                rear=0.0,
                rear_min=0.0,
                rear_max=0.0,
            ),
            brakes=Brakes(
                balance_pct=50.0,
                power_pct=100.0,
            ),
            differential=Differential(
                acceleration_front=50.0,
                deceleration_front=0.0,
                acceleration_rear=75.0,
                deceleration_rear=5.0,
                balance=63.0,
            ),
            assists=Assists(
                abs=False,
                stm=False,
                tcs=False,
                shifting="Manual",
                steering="Simulation",
            ),
        )

    @classmethod
    def as_dict(cls) -> dict[str, Any]:
        """Дефолты в виде вложенного словаря (для маппера/репозитория)."""
        return cls.create().model_dump(mode="json")

    @classmethod
    def get(cls, model_path: tuple[str, ...]) -> Any:
        """
        Возвращает дефолтное значение по пути модели.

        Пример:
            TuningDefaults.get(("tires", "front_pressure_bar"))  # → 2.0
            TuningDefaults.get(("brakes", "balance_pct"))        # → 50.0
        """
        current: Any = cls.as_dict()
        for key in model_path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current

    @classmethod
    def get_range(cls, model_path: tuple[str, ...]) -> tuple[float | None, float | None]:
        """
        Читает ge/le (ограничения) поля прямо из метаданных Pydantic v2 по пути в модели.
        Не требует изменений при добавлении новых полей — автоматически подхватывает
        новые ограничения из Field(ge=..., le=...).

        Пример:
            TuningDefaults.get_range(("tires", "front_pressure_bar"))  # → (1.0, 3.8)
            TuningDefaults.get_range(("brakes", "power_pct"))          # → (0.0, 200.0)
            TuningDefaults.get_range(("session", "name"))              # → (None, None)
        """
        from pydantic import BaseModel

        # Проходим по иерархии моделей до предпоследнего уровня
        model_cls: type[BaseModel] = TuningSetup
        for key in model_path[:-1]:
            field_info = model_cls.model_fields.get(key)
            if field_info is None:
                return None, None
            annotation = field_info.annotation
            if not (isinstance(annotation, type) and issubclass(annotation, BaseModel)):
                return None, None
            model_cls = annotation

        # Читаем FieldInfo целевого поля
        field_info = model_cls.model_fields.get(model_path[-1])
        if field_info is None:
            return None, None

        lo: float | None = None
        hi: float | None = None

        # Pydantic v2 хранит ограничения в field_info.metadata как annotated_types.Ge/.Le/.Gt/.Lt
        for constraint in field_info.metadata:
            if hasattr(constraint, "ge"):
                lo = float(constraint.ge)
            elif hasattr(constraint, "gt"):
                lo = float(constraint.gt)  # gt ≈ ge для слайдеров (целые шаги)
            if hasattr(constraint, "le"):
                hi = float(constraint.le)
            elif hasattr(constraint, "lt"):
                hi = float(constraint.lt)

        return lo, hi
