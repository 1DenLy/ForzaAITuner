from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String, Float, Boolean, DateTime, CheckConstraint, JSON
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, FLOAT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import text, event
from sqlalchemy import Enum as SQLAlchemyEnum
import enum

class CarClass(enum.Enum):
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S1 = "S1"
    S2 = "S2"
    X = "X"

class DrivetrainType(enum.Enum):
    RWD = "RWD"
    FWD = "FWD"
    AWD = "AWD"

class EngineLocation(enum.Enum):
    Front = "Front"
    Mid = "Mid"
    Rear = "Rear"

class MainBase(DeclarativeBase):
    pass

class TSBase(DeclarativeBase):
    pass

# 1. Машины
class Car(MainBase):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    game_ordinal: Mapped[int] = mapped_column(Integer, unique=True, index=True, comment="ID машины в файлах игры")
    nickname: Mapped[Optional[str]] = mapped_column(String(100))

    build_stats: Mapped[List["BuildStats"]] = relationship(back_populates="car")

# 2. Билд: Статистика (Hot Data)
class BuildStats(MainBase):
    __tablename__ = "build_stats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    
    pi_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    car_class: Mapped[CarClass] = mapped_column(SQLAlchemyEnum(CarClass), nullable=False)
    
    horsepower_kw: Mapped[int] = mapped_column(Integer)
    torque_nm: Mapped[int] = mapped_column(Integer)
    weight_kg: Mapped[int] = mapped_column(Integer)
    weight_dist_front: Mapped[float] = mapped_column(Float)
    
    drivetrain: Mapped[DrivetrainType] = mapped_column(SQLAlchemyEnum(DrivetrainType))
    engine_location: Mapped[EngineLocation] = mapped_column(SQLAlchemyEnum(EngineLocation))
    
    has_adjustable_aero_front: Mapped[bool] = mapped_column(Boolean, default=False)
    has_adjustable_aero_rear: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    car: Mapped["Car"] = relationship(back_populates="build_stats")
    parts: Mapped["BuildParts"] = relationship(back_populates="stats", uselist=False)
    tunes: Mapped[List["Tune"]] = relationship(back_populates="build")

# 3. Билд: Запчасти (Cold Data, JSONB)
class BuildParts(MainBase):
    __tablename__ = "build_parts"

    build_id: Mapped[int] = mapped_column(ForeignKey("build_stats.id"), primary_key=True)
    
    tire_compound: Mapped[str] = mapped_column(String(50))
    tire_width_front: Mapped[int] = mapped_column(Integer)
    tire_width_rear: Mapped[int] = mapped_column(Integer)
    
    engine_swap: Mapped[Optional[str]] = mapped_column(String(100))
    aspiration_swap: Mapped[Optional[str]] = mapped_column(String(50))
    body_kit: Mapped[Optional[str]] = mapped_column(String(100))

    # JSONB для мелких деталей (поршни, маховик и т.д.)
    engine_parts: Mapped[dict] = mapped_column(JSONB, default={})
    platform_parts: Mapped[dict] = mapped_column(JSONB, default={})
    drivetrain_parts: Mapped[dict] = mapped_column(JSONB, default={})

    stats: Mapped["BuildStats"] = relationship(back_populates="parts")

# 4. Настройки (Tunes)
class Tune(MainBase):
    __tablename__ = "tunes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    build_id: Mapped[int] = mapped_column(ForeignKey("build_stats.id"), nullable=False)
    
    name: Mapped[str] = mapped_column(String(100), default="Default Tune")
    description: Mapped[Optional[str]] = mapped_column(String)
    
    # Шины (Tires)
    tire_pressure_front: Mapped[float] = mapped_column(Float)
    tire_pressure_rear: Mapped[float] = mapped_column(Float)
    
    # Развал/Схождение (Alignment)
    camber_front: Mapped[float] = mapped_column(Float)
    camber_rear: Mapped[float] = mapped_column(Float)
    toe_front: Mapped[float] = mapped_column(Float)
    toe_rear: Mapped[float] = mapped_column(Float)
    caster: Mapped[float] = mapped_column(Float)

    # Стабилизаторы (Anti-roll Bars)
    arb_front: Mapped[float] = mapped_column(Float)
    arb_rear: Mapped[float] = mapped_column(Float)

    # Пружины (Suspension/Springs)
    spring_front: Mapped[float] = mapped_column(Float)
    spring_rear: Mapped[float] = mapped_column(Float)
    height_front: Mapped[float] = mapped_column(Float)
    height_rear: Mapped[float] = mapped_column(Float)

    # Амортизаторы (Damping)
    rebound_front: Mapped[float] = mapped_column(Float)
    rebound_rear: Mapped[float] = mapped_column(Float)
    bump_front: Mapped[float] = mapped_column(Float)
    bump_rear: Mapped[float] = mapped_column(Float)

    # Аэродинамика (Aerodynamics)
    aero_front: Mapped[float] = mapped_column(Float)
    aero_rear: Mapped[float] = mapped_column(Float)

    # Тормоза (Brakes)
    brake_balance: Mapped[float] = mapped_column(Float, default=0.5)
    brake_pressure: Mapped[float] = mapped_column(Float, default=1.0)

    # Дифференциал (Differential)
    diff_accel_front: Mapped[Optional[float]] = mapped_column(Float)
    diff_decel_front: Mapped[Optional[float]] = mapped_column(Float)
    diff_accel_rear: Mapped[Optional[float]] = mapped_column(Float)
    diff_decel_rear: Mapped[Optional[float]] = mapped_column(Float)
    diff_balance: Mapped[Optional[float]] = mapped_column(Float)

    # Помощники (Assists) - храним как JSONB или отдельные поля
    assists: Mapped[dict] = mapped_column(JSONB, default={})

    # Передачи (Gearing)
    final_drive: Mapped[float] = mapped_column(Float, default=3.5)
    gear_ratios: Mapped[list] = mapped_column(JSONB) # Список чисел
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    build: Mapped["BuildStats"] = relationship(back_populates="tunes")
    sessions: Mapped[List["Session"]] = relationship(back_populates="tune")

    __table_args__ = (
        CheckConstraint('tire_pressure_front > 0 AND tire_pressure_front < 10', name='check_tire_f_safe'),
        CheckConstraint('tire_pressure_rear > 0 AND tire_pressure_rear < 10', name='check_tire_r_safe'),
        CheckConstraint('camber_front BETWEEN -10 AND 10', name='check_camber_f'),
    )

# 5. Сессии
class Session(MainBase):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tune_id: Mapped[int] = mapped_column(ForeignKey("tunes.id"))
    
    track_name: Mapped[str] = mapped_column(String(150))
    weather_type: Mapped[str] = mapped_column(String(50))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    duration_seconds: Mapped[float] = mapped_column(Float)

    tune: Mapped["Tune"] = relationship(back_populates="sessions")
    # telemetry_logs removed due to physical database separation

# 6. Телеметрия (Массивы + TimeSeries ready)
class Telemetry(TSBase):
    __tablename__ = "telemetry"

    # Timescale требует, чтобы время было частью Primary Key
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    session_id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)

    # Общая физика
    speed_mps: Mapped[float] = mapped_column(FLOAT(precision=4)) 
    rpm: Mapped[int] = mapped_column(Integer)
    gear: Mapped[int] = mapped_column(Integer)

    # Векторы [X, Y, Z] распакованы для лучшего сжатия
    g_force_x: Mapped[float] = mapped_column(FLOAT(precision=4))
    g_force_y: Mapped[float] = mapped_column(FLOAT(precision=4))
    g_force_z: Mapped[float] = mapped_column(FLOAT(precision=4))

    body_yaw: Mapped[float] = mapped_column(FLOAT(precision=4))
    body_pitch: Mapped[float] = mapped_column(FLOAT(precision=4))
    body_roll: Mapped[float] = mapped_column(FLOAT(precision=4))

    # Колеса (Отдельные колонки для аналитики)
    # Ход подвески
    susp_travel_fl: Mapped[float] = mapped_column(FLOAT(precision=4))
    susp_travel_fr: Mapped[float] = mapped_column(FLOAT(precision=4))
    susp_travel_rl: Mapped[float] = mapped_column(FLOAT(precision=4))
    susp_travel_rr: Mapped[float] = mapped_column(FLOAT(precision=4))

    # Пробуксовка
    wheel_slip_fl: Mapped[float] = mapped_column(FLOAT(precision=4))
    wheel_slip_fr: Mapped[float] = mapped_column(FLOAT(precision=4))
    wheel_slip_rl: Mapped[float] = mapped_column(FLOAT(precision=4))
    wheel_slip_rr: Mapped[float] = mapped_column(FLOAT(precision=4))

    # Скорость вращения
    wheel_speed_fl: Mapped[float] = mapped_column(FLOAT(precision=4))
    wheel_speed_fr: Mapped[float] = mapped_column(FLOAT(precision=4))
    wheel_speed_rl: Mapped[float] = mapped_column(FLOAT(precision=4))
    wheel_speed_rr: Mapped[float] = mapped_column(FLOAT(precision=4))

    # Температура шин
    tire_temp_fl: Mapped[int] = mapped_column(Integer)
    tire_temp_fr: Mapped[int] = mapped_column(Integer)
    tire_temp_rl: Mapped[int] = mapped_column(Integer)
    tire_temp_rr: Mapped[int] = mapped_column(Integer)

    # Ввод
    input_throttle: Mapped[float] = mapped_column(FLOAT(precision=4))
    input_brake: Mapped[float] = mapped_column(FLOAT(precision=4))
    input_steer: Mapped[float] = mapped_column(FLOAT(precision=4))
    input_clutch: Mapped[float] = mapped_column(FLOAT(precision=4))
    input_handbrake: Mapped[bool] = mapped_column(Boolean)

    # session relationship removed due to physical database separation
# ==========================================
# ALEMBIC / TIMESCALEDB INSTRUCTIONS
# ==========================================
# Когда вы инициализируете Alembic (alembic init) для этой базы данных, 
# сгенерируйте первую миграцию (alembic revision --autogenerate), 
# и вручную добавьте следующий код в функцию upgrade():
#
# def upgrade() -> None:
#     # ... существующий код создания таблиц ...
#     op.execute("SELECT create_hypertable('telemetry', 'time', if_not_exists => TRUE);")
#     op.execute("ALTER TABLE telemetry SET (timescaledb.compress, timescaledb.compress_segmentby = 'session_id');")
# ==========================================