from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String, Float, Boolean, DateTime, CheckConstraint, JSON
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, FLOAT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

# 1. Машины
class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    game_ordinal: Mapped[int] = mapped_column(Integer, unique=True, index=True, comment="ID машины в файлах игры")
    nickname: Mapped[Optional[str]] = mapped_column(String(100))

    build_stats: Mapped[List["BuildStats"]] = relationship(back_populates="car")

# 2. Билд: Статистика (Hot Data)
class BuildStats(Base):
    __tablename__ = "build_stats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    
    pi_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    car_class: Mapped[str] = mapped_column(String(10), nullable=False) # Enum: A, S1, S2...
    
    horsepower_kw: Mapped[int] = mapped_column(Integer)
    torque_nm: Mapped[int] = mapped_column(Integer)
    weight_kg: Mapped[int] = mapped_column(Integer)
    weight_dist_front: Mapped[float] = mapped_column(Float)
    
    drivetrain: Mapped[str] = mapped_column(String(10)) # RWD, AWD
    engine_location: Mapped[str] = mapped_column(String(10))
    
    has_adjustable_aero_front: Mapped[bool] = mapped_column(Boolean, default=False)
    has_adjustable_aero_rear: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    car: Mapped["Car"] = relationship(back_populates="build_stats")
    parts: Mapped["BuildParts"] = relationship(back_populates="stats", uselist=False)
    tunes: Mapped[List["Tune"]] = relationship(back_populates="build")

# 3. Билд: Запчасти (Cold Data, JSONB)
class BuildParts(Base):
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

# 4. Настройки (Tunes) с защитой данных
class Tune(Base):
    __tablename__ = "tunes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    build_id: Mapped[int] = mapped_column(ForeignKey("build_stats.id"), nullable=False)
    
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String)
    
    # Constraints (Безопасность): Давление > 0 и < 10 бар
    tire_pressure_front: Mapped[float] = mapped_column(Float)
    tire_pressure_rear: Mapped[float] = mapped_column(Float)
    
    # Геометрия (-10 до +10 градусов)
    camber_front: Mapped[float] = mapped_column(Float)
    camber_rear: Mapped[float] = mapped_column(Float)
    
    gear_ratios: Mapped[list] = mapped_column(JSONB) # Список чисел
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    build: Mapped["BuildStats"] = relationship(back_populates="tunes")
    sessions: Mapped[List["Session"]] = relationship(back_populates="tune")

    __table_args__ = (
        CheckConstraint('tire_pressure_front > 0 AND tire_pressure_front < 10', name='check_tire_f_safe'),
        CheckConstraint('tire_pressure_rear > 0 AND tire_pressure_rear < 10', name='check_tire_r_safe'),
    )

# 5. Сессии
class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tune_id: Mapped[int] = mapped_column(ForeignKey("tunes.id"))
    
    track_name: Mapped[str] = mapped_column(String(150))
    weather_type: Mapped[str] = mapped_column(String(50))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    duration_seconds: Mapped[float] = mapped_column(Float)

    tune: Mapped["Tune"] = relationship(back_populates="sessions")
    # cascade="all, delete" нужно для очистки телеметрии при удалении сессии
    telemetry_logs: Mapped[List["Telemetry"]] = relationship(back_populates="session", cascade="all, delete-orphan")

# 6. Телеметрия (Массивы + TimeSeries ready)
class Telemetry(Base):
    __tablename__ = "telemetry"

    # Timescale требует, чтобы время было частью Primary Key
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), primary_key=True)

    # Общая физика
    speed_mps: Mapped[float] = mapped_column(FLOAT(precision=4)) 
    rpm: Mapped[int] = mapped_column(Integer)
    gear: Mapped[int] = mapped_column(Integer)

    # Векторы [X, Y, Z]
    g_force: Mapped[List[float]] = mapped_column(ARRAY(FLOAT(precision=4))) 
    body_angles: Mapped[List[float]] = mapped_column(ARRAY(FLOAT(precision=4)))

    # Колеса [FL, FR, RL, RR]
    susp_travel: Mapped[List[float]] = mapped_column(ARRAY(FLOAT(precision=4)))
    wheel_slip: Mapped[List[float]] = mapped_column(ARRAY(FLOAT(precision=4)))
    wheel_speed: Mapped[List[float]] = mapped_column(ARRAY(FLOAT(precision=4)))
    tire_temp: Mapped[List[int]] = mapped_column(ARRAY(Integer))

    # Ввод
    input_throttle: Mapped[float] = mapped_column(FLOAT(precision=4))
    input_brake: Mapped[float] = mapped_column(FLOAT(precision=4))
    input_steer: Mapped[float] = mapped_column(FLOAT(precision=4))
    input_clutch: Mapped[float] = mapped_column(FLOAT(precision=4))
    input_handbrake: Mapped[bool] = mapped_column(Boolean)

    session: Mapped["Session"] = relationship(back_populates="telemetry_logs")

# ==========================================
# AUTO-MIGRATION: Превращаем таблицу в Hypertable
# ==========================================
def after_telemetry_create(target, connection, **kw):
    """
    Выполняется автоматически сразу после создания таблицы telemetry.
    Превращает обычную таблицу в TimescaleDB Hypertable.
    """
    print("Converting 'telemetry' to TimescaleDB Hypertable...")
    connection.execute(text(
        "SELECT create_hypertable('telemetry', 'time', if_not_exists => TRUE);"
    ))
    
    # Опционально: Включаем сжатие данных (для экономии места в 10+ раз)
    # Сжимаем данные старше 7 дней
    try:
        connection.execute(text(
            "ALTER TABLE telemetry SET (timescaledb.compress, timescaledb.compress_segmentby = 'session_id');"
        ))
        # Политика сжатия добавляется отдельно, обычно через cron jobs, 
        # но включить саму возможность сжатия лучше сразу.
    except Exception as e:
        print(f"Warning: Could not enable compression (maybe already enabled?): {e}")

# Подписываемся на событие создания таблицы
event.listen(Telemetry.__table__, 'after_create', after_telemetry_create)