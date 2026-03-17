from datetime import datetime
import uuid
from sqlalchemy import Integer, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import UUID, FLOAT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class TSBase(DeclarativeBase):
    pass

class Telemetry(TSBase):
    """
    Telemetry data model aligned exactly with Forza Horizon 4/5 packet format.
    Names and documentation are derived from docs/DataBase/tsdb/FH4_packetformat.dat
    """
    __tablename__ = "telemetry"

    # --- Database Internal Fields (TimescaleDB) ---
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, primary_key=True)
    tuning_config_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), index=True, nullable=True)

    # --- Packet Data (Exact Names) ---
    IsRaceOn: Mapped[int] = mapped_column(Integer)  # = 1 when race is on. = 0 when in menus/race stopped
    TimestampMS: Mapped[int] = mapped_column(BigInteger)  # Can overflow to 0 eventually. [ms]
    EngineMaxRpm: Mapped[float] = mapped_column(FLOAT(precision=4))
    EngineIdleRpm: Mapped[float] = mapped_column(FLOAT(precision=4))
    CurrentEngineRpm: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # In the car's local space; X = right, Y = up, Z = forward
    AccelerationX: Mapped[float] = mapped_column(FLOAT(precision=4))
    AccelerationY: Mapped[float] = mapped_column(FLOAT(precision=4))
    AccelerationZ: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # In the car's local space; X = right, Y = up, Z = forward
    VelocityX: Mapped[float] = mapped_column(FLOAT(precision=4))
    VelocityY: Mapped[float] = mapped_column(FLOAT(precision=4))
    VelocityZ: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # In the car's local space; X = pitch, Y = yaw, Z = roll
    AngularVelocityX: Mapped[float] = mapped_column(FLOAT(precision=4))
    AngularVelocityY: Mapped[float] = mapped_column(FLOAT(precision=4))
    AngularVelocityZ: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    Yaw: Mapped[float] = mapped_column(FLOAT(precision=4))
    Pitch: Mapped[float] = mapped_column(FLOAT(precision=4))
    Roll: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # Suspension travel normalized: 0.0f = max stretch; 1.0 = max compression
    NormalizedSuspensionTravelFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    NormalizedSuspensionTravelFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    NormalizedSuspensionTravelRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    NormalizedSuspensionTravelRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # Tire normalized slip ratio, = 0 means 100% grip and |ratio| > 1.0 means loss of grip.
    TireSlipRatioFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireSlipRatioFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireSlipRatioRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireSlipRatioRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # Wheel rotation speed radians/sec.
    WheelRotationSpeedFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    WheelRotationSpeedFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    WheelRotationSpeedRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    WheelRotationSpeedRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # = 1 when wheel is on rumble strip, = 0 when off.
    WheelOnRumbleStripFrontLeft: Mapped[int] = mapped_column(Integer)
    WheelOnRumbleStripFrontRight: Mapped[int] = mapped_column(Integer)
    WheelOnRumbleStripRearLeft: Mapped[int] = mapped_column(Integer)
    WheelOnRumbleStripRearRight: Mapped[int] = mapped_column(Integer)
    
    # = from 0 to 1, where 1 is the deepest puddle
    WheelInPuddleDepthFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    WheelInPuddleDepthFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    WheelInPuddleDepthRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    WheelInPuddleDepthRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # Non-dimensional surface rumble values passed to controller force feedback
    SurfaceRumbleFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    SurfaceRumbleFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    SurfaceRumbleRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    SurfaceRumbleRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # Tire normalized slip angle, = 0 means 100% grip and |angle| > 1.0 means loss of grip.
    TireSlipAngleFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireSlipAngleFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireSlipAngleRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireSlipAngleRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # Tire normalized combined slip, = 0 means 100% grip and |slip| > 1.0 means loss of grip.
    TireCombinedSlipFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireCombinedSlipFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireCombinedSlipRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireCombinedSlipRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    # Actual suspension travel in meters
    SuspensionTravelMetersFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    SuspensionTravelMetersFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    SuspensionTravelMetersRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    SuspensionTravelMetersRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    CarOrdinal: Mapped[int] = mapped_column(Integer)  # Unique ID of the car make/model
    CarClass: Mapped[int] = mapped_column(Integer)  # Between 0 (D) and 7 (X class)
    CarPerformanceIndex: Mapped[int] = mapped_column(Integer)  # Between 100 and 999
    DrivetrainType: Mapped[int] = mapped_column(Integer)  # 0 = FWD, 1 = RWD, 2 = AWD
    NumCylinders: Mapped[int] = mapped_column(Integer)  # Number of cylinders in the engine
    
    HorizonPlaceholder: Mapped[int] = mapped_column(Integer, nullable=True)  # unknown FH4 values
    
    PositionX: Mapped[float] = mapped_column(FLOAT(precision=4))
    PositionY: Mapped[float] = mapped_column(FLOAT(precision=4))
    PositionZ: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    Speed: Mapped[float] = mapped_column(FLOAT(precision=4))  # [meters per second]
    Power: Mapped[float] = mapped_column(FLOAT(precision=4))  # [watts]
    Torque: Mapped[float] = mapped_column(FLOAT(precision=4))  # [newton meter]
    
    TireTempFrontLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireTempFrontRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireTempRearLeft: Mapped[float] = mapped_column(FLOAT(precision=4))
    TireTempRearRight: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    Boost: Mapped[float] = mapped_column(FLOAT(precision=4))
    Fuel: Mapped[float] = mapped_column(FLOAT(precision=4))
    DistanceTraveled: Mapped[float] = mapped_column(FLOAT(precision=4))
    BestLap: Mapped[float] = mapped_column(FLOAT(precision=4))
    LastLap: Mapped[float] = mapped_column(FLOAT(precision=4))
    CurrentLap: Mapped[float] = mapped_column(FLOAT(precision=4))
    CurrentRaceTime: Mapped[float] = mapped_column(FLOAT(precision=4))
    
    LapNumber: Mapped[int] = mapped_column(Integer)
    RacePosition: Mapped[int] = mapped_column(Integer)
    Accel: Mapped[int] = mapped_column(Integer)  # [0-255]
    Brake: Mapped[int] = mapped_column(Integer)  # [0-255]
    Clutch: Mapped[int] = mapped_column(Integer)  # [0-255]
    HandBrake: Mapped[int] = mapped_column(Integer)  # [0-255]
    Gear: Mapped[int] = mapped_column(Integer)  # [0-15]
    Steer: Mapped[int] = mapped_column(Integer)  # [-127 to 127]
    NormalizedDrivingLine: Mapped[int] = mapped_column(Integer)
    NormalizedAIBrakeDifference: Mapped[int] = mapped_column(Integer)
