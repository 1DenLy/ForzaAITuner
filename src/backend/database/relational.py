from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import ForeignKey, Integer, String, Float, Boolean, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

class MainBase(DeclarativeBase):
    pass

# --- 1. Таблица users (Пользователи) ---
class User(MainBase):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sessions: Mapped[List["Session"]] = relationship(back_populates="user")

# --- 2. Таблица cars (Автомобили) ---
class Car(MainBase):
    __tablename__ = "cars"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forza_ordinal: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    engine_placement: Mapped[str] = mapped_column(String(50))

    sessions: Mapped[List["Session"]] = relationship(back_populates="car")

# --- 3. Таблица sessions (Заезды) ---
class Session(MainBase):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    car_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cars.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(255))
    surface: Mapped[str] = mapped_column(String(100))
    road_type: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="sessions")
    car: Mapped["Car"] = relationship(back_populates="sessions")
    assists: Mapped["SessionAssists"] = relationship(back_populates="session", uselist=False)
    configs: Mapped[List["Config"]] = relationship(back_populates="session")

# --- 3.1 Таблица session_assists (Помощники) ---
class SessionAssists(MainBase):
    __tablename__ = "session_assists"

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"), primary_key=True)
    abs: Mapped[bool] = mapped_column(Boolean)
    stm: Mapped[bool] = mapped_column(Boolean)
    tcs: Mapped[bool] = mapped_column(Boolean)
    shifting: Mapped[str] = mapped_column(String(50))
    steering: Mapped[str] = mapped_column(String(50))

    session: Mapped["Session"] = relationship(back_populates="assists")

# --- 4. Таблица configs (Базовая информация) ---
class Config(MainBase):
    __tablename__ = "configs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Характеристики (Inputs)
    weight: Mapped[int] = mapped_column(Integer)
    power: Mapped[int] = mapped_column(Integer)
    torque: Mapped[int] = mapped_column(Integer)
    front_weight: Mapped[float] = mapped_column(Float)
    suspension_travel: Mapped[int] = mapped_column(Integer)
    drive_type: Mapped[str] = mapped_column(String(10))
    class_pi: Mapped[int] = mapped_column(Integer)

    session: Mapped["Session"] = relationship(back_populates="configs")
    
    # 1:1 Relationships to sub-configs
    tires: Mapped["ConfigTires"] = relationship(back_populates="config", uselist=False)
    anti_roll_bars: Mapped["ConfigAntiRollBars"] = relationship(back_populates="config", uselist=False)
    suspension: Mapped["ConfigSuspension"] = relationship(back_populates="config", uselist=False)
    damping: Mapped["ConfigDamping"] = relationship(back_populates="config", uselist=False)
    aerodynamics: Mapped["ConfigAerodynamics"] = relationship(back_populates="config", uselist=False)
    gearing: Mapped["ConfigGearing"] = relationship(back_populates="config", uselist=False)
    alignment: Mapped["ConfigAlignment"] = relationship(back_populates="config", uselist=False)
    differential: Mapped["ConfigDifferential"] = relationship(back_populates="config", uselist=False)
    brakes: Mapped["ConfigBrakes"] = relationship(back_populates="config", uselist=False)

    __table_args__ = (
        CheckConstraint('weight >= 1', name='check_weight_min'),
        CheckConstraint('power >= 1', name='check_power_min'),
        CheckConstraint('torque >= 1', name='check_torque_min'),
        CheckConstraint('front_weight BETWEEN 0.0 AND 100.0', name='check_front_weight_range'),
        CheckConstraint('suspension_travel >= 1', name='check_suspension_travel_min'),
        CheckConstraint('class_pi BETWEEN 100 AND 999', name='check_class_pi_range'),
    )

class ConfigTires(MainBase):
    __tablename__ = "config_tires"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    front_pressure_bar: Mapped[float] = mapped_column(Float)
    rear_pressure_bar: Mapped[float] = mapped_column(Float)
    width_front: Mapped[int] = mapped_column(Integer)
    width_rear: Mapped[int] = mapped_column(Integer)
    compound: Mapped[str] = mapped_column(String(100))
    config: Mapped["Config"] = relationship(back_populates="tires")
    __table_args__ = (
        CheckConstraint('front_pressure_bar BETWEEN 1.0 AND 3.8', name='check_tire_pressure_f'),
        CheckConstraint('rear_pressure_bar BETWEEN 1.0 AND 3.8', name='check_tire_pressure_r'),
        CheckConstraint('width_front >= 1', name='check_width_front_min'),
        CheckConstraint('width_rear >= 1', name='check_width_rear_min'),
    )

class ConfigAntiRollBars(MainBase):
    __tablename__ = "config_anti_roll_bars"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    front: Mapped[float] = mapped_column(Float)
    rear: Mapped[float] = mapped_column(Float)
    config: Mapped["Config"] = relationship(back_populates="anti_roll_bars")
    __table_args__ = (
        CheckConstraint('front BETWEEN 1.0 AND 65.0', name='check_arb_front'),
        CheckConstraint('rear BETWEEN 1.0 AND 65.0', name='check_arb_rear'),
    )

class ConfigSuspension(MainBase):
    __tablename__ = "config_suspension"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    spring_front: Mapped[float] = mapped_column(Float)
    spring_rear: Mapped[float] = mapped_column(Float)
    spring_min: Mapped[float] = mapped_column(Float)
    spring_max: Mapped[float] = mapped_column(Float)
    clearance_front: Mapped[float] = mapped_column(Float)
    clearance_rear: Mapped[float] = mapped_column(Float)
    clearance_min: Mapped[float] = mapped_column(Float)
    clearance_max: Mapped[float] = mapped_column(Float)
    config: Mapped["Config"] = relationship(back_populates="suspension")
    __table_args__ = (
        CheckConstraint('spring_front >= 0.1', name='check_spring_f'),
        CheckConstraint('spring_rear >= 0.1', name='check_spring_r'),
        CheckConstraint('spring_min >= 0.1', name='check_spring_min'),
        CheckConstraint('spring_max >= 0.1', name='check_spring_max'),
        CheckConstraint('clearance_front >= 0.1', name='check_clearance_f'),
        CheckConstraint('clearance_rear >= 0.1', name='check_clearance_r'),
        CheckConstraint('clearance_min >= 0.1', name='check_clearance_min'),
        CheckConstraint('clearance_max >= 0.1', name='check_clearance_max'),
    )

class ConfigDamping(MainBase):
    __tablename__ = "config_damping"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    rebound_front: Mapped[float] = mapped_column(Float)
    rebound_rear: Mapped[float] = mapped_column(Float)
    rebound_min: Mapped[float] = mapped_column(Float)
    rebound_max: Mapped[float] = mapped_column(Float)
    bump_front: Mapped[float] = mapped_column(Float)
    bump_rear: Mapped[float] = mapped_column(Float)
    bump_min: Mapped[float] = mapped_column(Float)
    bump_max: Mapped[float] = mapped_column(Float)
    config: Mapped["Config"] = relationship(back_populates="damping")
    __table_args__ = (
        CheckConstraint('rebound_front BETWEEN 1.0 AND 20.0', name='check_rebound_f'),
        CheckConstraint('rebound_rear BETWEEN 1.0 AND 20.0', name='check_rebound_r'),
        CheckConstraint('rebound_min BETWEEN 1.0 AND 20.0', name='check_rebound_min'),
        CheckConstraint('rebound_max BETWEEN 1.0 AND 20.0', name='check_rebound_max'),
        CheckConstraint('bump_front BETWEEN 1.0 AND 20.0', name='check_bump_f'),
        CheckConstraint('bump_rear BETWEEN 1.0 AND 20.0', name='check_bump_r'),
        CheckConstraint('bump_min BETWEEN 1.0 AND 20.0', name='check_bump_min'),
        CheckConstraint('bump_max BETWEEN 1.0 AND 20.0', name='check_bump_max'),
    )

class ConfigAerodynamics(MainBase):
    __tablename__ = "config_aerodynamics"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    front: Mapped[float] = mapped_column(Float)
    rear: Mapped[float] = mapped_column(Float)
    front_min: Mapped[float] = mapped_column(Float)
    front_max: Mapped[float] = mapped_column(Float)
    rear_min: Mapped[float] = mapped_column(Float)
    rear_max: Mapped[float] = mapped_column(Float)
    front_enabled: Mapped[bool] = mapped_column(Boolean)
    rear_enabled: Mapped[bool] = mapped_column(Boolean)
    config: Mapped["Config"] = relationship(back_populates="aerodynamics")
    __table_args__ = (
        CheckConstraint('front >= 1.0', name='check_aero_front'),
        CheckConstraint('front_min >= 1.0', name='check_aero_front_min'),
        CheckConstraint('front_max >= 1.0', name='check_aero_front_max'),
        CheckConstraint('rear >= 1.0', name='check_aero_rear'),
        CheckConstraint('rear_min >= 1.0', name='check_aero_rear_min'),
        CheckConstraint('rear_max >= 1.0', name='check_aero_rear_max'),
    )

class ConfigGearing(MainBase):
    __tablename__ = "config_gearing"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    final_drive: Mapped[float] = mapped_column(Float)
    gears: Mapped[list] = mapped_column(JSONB)
    config: Mapped["Config"] = relationship(back_populates="gearing")
    __table_args__ = (
        CheckConstraint('final_drive >= 0.1', name='check_final_drive_min'),
    )

class ConfigAlignment(MainBase):
    __tablename__ = "config_alignment"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    camber_front_deg: Mapped[float] = mapped_column(Float)
    camber_rear_deg: Mapped[float] = mapped_column(Float)
    toe_front_deg: Mapped[float] = mapped_column(Float)
    toe_rear_deg: Mapped[float] = mapped_column(Float)
    caster_front_deg: Mapped[float] = mapped_column(Float)
    config: Mapped["Config"] = relationship(back_populates="alignment")
    __table_args__ = (
        CheckConstraint('camber_front_deg BETWEEN -5.0 AND 5.0', name='check_camber_f'),
        CheckConstraint('camber_rear_deg BETWEEN -5.0 AND 5.0', name='check_camber_r'),
        CheckConstraint('toe_front_deg BETWEEN -5.0 AND 5.0', name='check_toe_f'),
        CheckConstraint('toe_rear_deg BETWEEN -5.0 AND 5.0', name='check_toe_r'),
        CheckConstraint('caster_front_deg BETWEEN 1.0 AND 7.0', name='check_caster'),
    )

class ConfigDifferential(MainBase):
    __tablename__ = "config_differential"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    acceleration_front: Mapped[float] = mapped_column(Float)
    deceleration_front: Mapped[float] = mapped_column(Float)
    acceleration_rear: Mapped[float] = mapped_column(Float)
    deceleration_rear: Mapped[float] = mapped_column(Float)
    balance: Mapped[float] = mapped_column(Float)
    config: Mapped["Config"] = relationship(back_populates="differential")
    __table_args__ = (
        CheckConstraint('acceleration_front BETWEEN 0.0 AND 100.0', name='check_diff_accel_f'),
        CheckConstraint('deceleration_front BETWEEN 0.0 AND 100.0', name='check_diff_decel_f'),
        CheckConstraint('acceleration_rear BETWEEN 0.0 AND 100.0', name='check_diff_accel_r'),
        CheckConstraint('deceleration_rear BETWEEN 0.0 AND 100.0', name='check_diff_decel_r'),
        CheckConstraint('balance BETWEEN 0.0 AND 100.0', name='check_diff_balance'),
    )

class ConfigBrakes(MainBase):
    __tablename__ = "config_brakes"
    config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("configs.id"), primary_key=True)
    balance_pct: Mapped[float] = mapped_column(Float)
    power_pct: Mapped[float] = mapped_column(Float)
    config: Mapped["Config"] = relationship(back_populates="brakes")
    __table_args__ = (
        CheckConstraint('balance_pct BETWEEN 0.0 AND 100.0', name='check_brake_balance'),
        CheckConstraint('power_pct BETWEEN 0.0 AND 200.0', name='check_brake_pressure'),
    )
