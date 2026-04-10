from .models import RawTelemetry
from ..domain.models import TelemetryPacket


class PacketParser:
    """
    IPacketParser implementation: pure field mapping from RawTelemetry to TelemetryPacket.

    Responsibilities:
    - Transfer fields from RawTelemetry to TelemetryPacket.
    - No validation. If RawTelemetry contains NaN, it is mapped faithfully.
    - All accept/reject decisions belong to IPacketValidator.

    Does NOT:
    - Check NaN, Inf, or anomalous values.
    - Work with raw bytes.
    - Drop packets.
    """

    def parse(self, raw: RawTelemetry) -> TelemetryPacket:
        """
        Maps RawTelemetry fields to the TelemetryPacket domain model.

        Raises:
            TypeError  — if a field has an unexpected type (routed to DLQ as PARSE_ERROR).
        """
        return TelemetryPacket(
            IsRaceOn=raw.IsRaceOn,
            TimestampMS=raw.TimestampMS,
            EngineMaxRpm=raw.EngineMaxRpm,
            EngineIdleRpm=raw.EngineIdleRpm,
            CurrentEngineRpm=raw.CurrentEngineRpm,
            AccelerationX=raw.AccelerationX,
            AccelerationY=raw.AccelerationY,
            AccelerationZ=raw.AccelerationZ,
            VelocityX=raw.VelocityX,
            VelocityY=raw.VelocityY,
            VelocityZ=raw.VelocityZ,
            AngularVelocityX=raw.AngularVelocityX,
            AngularVelocityY=raw.AngularVelocityY,
            AngularVelocityZ=raw.AngularVelocityZ,
            Yaw=raw.Yaw,
            Pitch=raw.Pitch,
            Roll=raw.Roll,
            NormalizedSuspensionTravelFrontLeft=raw.NormalizedSuspensionTravelFrontLeft,
            NormalizedSuspensionTravelFrontRight=raw.NormalizedSuspensionTravelFrontRight,
            NormalizedSuspensionTravelRearLeft=raw.NormalizedSuspensionTravelRearLeft,
            NormalizedSuspensionTravelRearRight=raw.NormalizedSuspensionTravelRearRight,
            TireSlipRatioFrontLeft=raw.TireSlipRatioFrontLeft,
            TireSlipRatioFrontRight=raw.TireSlipRatioFrontRight,
            TireSlipRatioRearLeft=raw.TireSlipRatioRearLeft,
            TireSlipRatioRearRight=raw.TireSlipRatioRearRight,
            WheelRotationSpeedFrontLeft=raw.WheelRotationSpeedFrontLeft,
            WheelRotationSpeedFrontRight=raw.WheelRotationSpeedFrontRight,
            WheelRotationSpeedRearLeft=raw.WheelRotationSpeedRearLeft,
            WheelRotationSpeedRearRight=raw.WheelRotationSpeedRearRight,
            WheelOnRumbleStripFrontLeft=raw.WheelOnRumbleStripFrontLeft,
            WheelOnRumbleStripFrontRight=raw.WheelOnRumbleStripFrontRight,
            WheelOnRumbleStripRearLeft=raw.WheelOnRumbleStripRearLeft,
            WheelOnRumbleStripRearRight=raw.WheelOnRumbleStripRearRight,
            WheelInPuddleDepthFrontLeft=raw.WheelInPuddleDepthFrontLeft,
            WheelInPuddleDepthFrontRight=raw.WheelInPuddleDepthFrontRight,
            WheelInPuddleDepthRearLeft=raw.WheelInPuddleDepthRearLeft,
            WheelInPuddleDepthRearRight=raw.WheelInPuddleDepthRearRight,
            SurfaceRumbleFrontLeft=raw.SurfaceRumbleFrontLeft,
            SurfaceRumbleFrontRight=raw.SurfaceRumbleFrontRight,
            SurfaceRumbleRearLeft=raw.SurfaceRumbleRearLeft,
            SurfaceRumbleRearRight=raw.SurfaceRumbleRearRight,
            TireSlipAngleFrontLeft=raw.TireSlipAngleFrontLeft,
            TireSlipAngleFrontRight=raw.TireSlipAngleFrontRight,
            TireSlipAngleRearLeft=raw.TireSlipAngleRearLeft,
            TireSlipAngleRearRight=raw.TireSlipAngleRearRight,
            TireCombinedSlipFrontLeft=raw.TireCombinedSlipFrontLeft,
            TireCombinedSlipFrontRight=raw.TireCombinedSlipFrontRight,
            TireCombinedSlipRearLeft=raw.TireCombinedSlipRearLeft,
            TireCombinedSlipRearRight=raw.TireCombinedSlipRearRight,
            SuspensionTravelMetersFrontLeft=raw.SuspensionTravelMetersFrontLeft,
            SuspensionTravelMetersFrontRight=raw.SuspensionTravelMetersFrontRight,
            SuspensionTravelMetersRearLeft=raw.SuspensionTravelMetersRearLeft,
            SuspensionTravelMetersRearRight=raw.SuspensionTravelMetersRearRight,
            CarOrdinal=raw.CarOrdinal,
            CarClass=raw.CarClass,
            CarPerformanceIndex=raw.CarPerformanceIndex,
            DrivetrainType=raw.DrivetrainType,
            NumCylinders=raw.NumCylinders,
            HorizonPlaceholder=raw.HorizonPlaceholder,
            PositionX=raw.PositionX,
            PositionY=raw.PositionY,
            PositionZ=raw.PositionZ,
            Speed=raw.Speed,
            Power=raw.Power,
            Torque=raw.Torque,
            TireTempFrontLeft=raw.TireTempFrontLeft,
            TireTempFrontRight=raw.TireTempFrontRight,
            TireTempRearLeft=raw.TireTempRearLeft,
            TireTempRearRight=raw.TireTempRearRight,
            Boost=raw.Boost,
            Fuel=raw.Fuel,
            DistanceTraveled=raw.DistanceTraveled,
            BestLap=raw.BestLap,
            LastLap=raw.LastLap,
            CurrentLap=raw.CurrentLap,
            CurrentRaceTime=raw.CurrentRaceTime,
            LapNumber=raw.LapNumber,
            RacePosition=raw.RacePosition,
            Accel=raw.Accel,
            Brake=raw.Brake,
            Clutch=raw.Clutch,
            HandBrake=raw.HandBrake,
            Gear=raw.Gear,
            Steer=raw.Steer,
            NormalizedDrivingLine=raw.NormalizedDrivingLine,
            NormalizedAIBrakeDifference=raw.NormalizedAIBrakeDifference,
        )
