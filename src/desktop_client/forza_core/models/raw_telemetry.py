import dataclasses
from datetime import datetime


@dataclasses.dataclass(frozen=True, slots=True)
class RawTelemetry:
    """
    Primitives unpacked from a Forza telemetry packet via struct.unpack.

    Produced by: IPacketDecoder.decode(bytes) — binary decoding only.
    Consumed by: IPacketParser.parse(RawTelemetry) — domain mapping.

    This is NOT a domain model. It contains raw numeric types exactly as
    unpacked from the binary format, without any semantic transformation.
    The received_at timestamp is forwarded from RawPacket for traceability.

    Field order matches the Forza telemetry binary format (little-endian).
    """
    # Forwarded from RawPacket
    received_at: datetime

    # s32 — 1 when race is on, 0 in menu/stopped
    IsRaceOn: int

    # u32 — can overflow to 0 eventually [ms]
    TimestampMS: int

    EngineMaxRpm: float
    EngineIdleRpm: float
    CurrentEngineRpm: float

    # Car's local space: X=right, Y=up, Z=forward [m/s²]
    AccelerationX: float
    AccelerationY: float
    AccelerationZ: float

    # Car's local space: X=right, Y=up, Z=forward [m/s]
    VelocityX: float
    VelocityY: float
    VelocityZ: float

    # Car's local space: X=pitch, Y=yaw, Z=roll [rad/s]
    AngularVelocityX: float
    AngularVelocityY: float
    AngularVelocityZ: float

    Yaw: float
    Pitch: float
    Roll: float

    # 0.0=max stretch, 1.0=max compression
    NormalizedSuspensionTravelFrontLeft: float
    NormalizedSuspensionTravelFrontRight: float
    NormalizedSuspensionTravelRearLeft: float
    NormalizedSuspensionTravelRearRight: float

    # 0=100% grip, |ratio|>1.0=loss of grip
    TireSlipRatioFrontLeft: float
    TireSlipRatioFrontRight: float
    TireSlipRatioRearLeft: float
    TireSlipRatioRearRight: float

    # [rad/s]
    WheelRotationSpeedFrontLeft: float
    WheelRotationSpeedFrontRight: float
    WheelRotationSpeedRearLeft: float
    WheelRotationSpeedRearRight: float

    # 1=on rumble strip, 0=off
    WheelOnRumbleStripFrontLeft: int
    WheelOnRumbleStripFrontRight: int
    WheelOnRumbleStripRearLeft: int
    WheelOnRumbleStripRearRight: int

    # 0..1, 1=deepest puddle
    WheelInPuddleDepthFrontLeft: float
    WheelInPuddleDepthFrontRight: float
    WheelInPuddleDepthRearLeft: float
    WheelInPuddleDepthRearRight: float

    SurfaceRumbleFrontLeft: float
    SurfaceRumbleFrontRight: float
    SurfaceRumbleRearLeft: float
    SurfaceRumbleRearRight: float

    # 0=100% grip, |angle|>1.0=loss of grip
    TireSlipAngleFrontLeft: float
    TireSlipAngleFrontRight: float
    TireSlipAngleRearLeft: float
    TireSlipAngleRearRight: float

    TireCombinedSlipFrontLeft: float
    TireCombinedSlipFrontRight: float
    TireCombinedSlipRearLeft: float
    TireCombinedSlipRearRight: float

    # Actual suspension travel [m]
    SuspensionTravelMetersFrontLeft: float
    SuspensionTravelMetersFrontRight: float
    SuspensionTravelMetersRearLeft: float
    SuspensionTravelMetersRearRight: float

    # Unique ID of car make/model
    CarOrdinal: int
    # 0=D, 7=X class
    CarClass: int
    # 100..999
    CarPerformanceIndex: int
    # 0=FWD, 1=RWD, 2=AWD
    DrivetrainType: int
    NumCylinders: int

    PositionX: float
    PositionY: float
    PositionZ: float

    Speed: float    # [m/s]
    Power: float    # [watts]
    Torque: float   # [newton meter]

    TireTempFrontLeft: float
    TireTempFrontRight: float
    TireTempRearLeft: float
    TireTempRearRight: float

    Boost: float
    Fuel: float
    DistanceTraveled: float
    BestLap: float
    LastLap: float
    CurrentLap: float
    CurrentRaceTime: float

    LapNumber: int      # u16
    RacePosition: int   # u8
    Accel: int          # u8 [0-255]
    Brake: int          # u8 [0-255]
    Clutch: int         # u8 [0-255]
    HandBrake: int      # u8 [0-255]
    Gear: int           # u8 [0-15]
    Steer: int          # s8 [-127..127]
    NormalizedDrivingLine: int      # s8
    NormalizedAIBrakeDifference: int  # s8

    # FH4/FH5 extended fields (None for FM7)
    HorizonPlaceholder: int | None = None   # u32 — undocumented FH4 gap
    # FH5 only
    TireTempFadeFL: float | None = None
    TireTempFadeFR: float | None = None
    TireTempFadeRL: float | None = None
    TireTempFadeRR: float | None = None
