import struct
from datetime import datetime, timezone

from ..interfaces import IPacketDecoder
from ..models import RawTelemetry


# Forza Motorsport 7 / "Dash" format — 311 bytes, little-endian.
# Source: docs/DataBase/tsdb/FH4_packetformat.dat, verified against
# existing codebase struct layout.
_FM7_FORMAT = (
    '<'
    'i'    # s32  IsRaceOn
    'I'    # u32  TimestampMS
    'f'    # f32  EngineMaxRpm
    'f'    # f32  EngineIdleRpm
    'f'    # f32  CurrentEngineRpm
    'fff'  # f32  AccelerationX/Y/Z
    'fff'  # f32  VelocityX/Y/Z
    'fff'  # f32  AngularVelocityX/Y/Z
    'fff'  # f32  Yaw, Pitch, Roll
    'ffff' # f32  NormSuspTravel FL/FR/RL/RR
    'ffff' # f32  TireSlipRatio FL/FR/RL/RR
    'ffff' # f32  WheelRotSpeed FL/FR/RL/RR
    'iiii' # s32  WheelOnRumble FL/FR/RL/RR
    'ffff' # f32  WheelInPuddle FL/FR/RL/RR
    'ffff' # f32  SurfaceRumble FL/FR/RL/RR
    'ffff' # f32  TireSlipAngle FL/FR/RL/RR
    'ffff' # f32  TireCombSlip FL/FR/RL/RR
    'ffff' # f32  SuspTravelMeters FL/FR/RL/RR
    'i'    # s32  CarOrdinal
    'i'    # s32  CarClass
    'i'    # s32  CarPerformanceIndex
    'i'    # s32  DrivetrainType
    'i'    # s32  NumCylinders
    'fff'  # f32  PositionX/Y/Z
    'f'    # f32  Speed
    'f'    # f32  Power
    'f'    # f32  Torque
    'ffff' # f32  TireTemp FL/FR/RL/RR
    'f'    # f32  Boost
    'f'    # f32  Fuel
    'f'    # f32  DistanceTraveled
    'f'    # f32  BestLap
    'f'    # f32  LastLap
    'f'    # f32  CurrentLap
    'f'    # f32  CurrentRaceTime
    'H'    # u16  LapNumber
    'B'    # u8   RacePosition
    'B'    # u8   Accel
    'B'    # u8   Brake
    'B'    # u8   Clutch
    'B'    # u8   HandBrake
    'B'    # u8   Gear
    'b'    # s8   Steer
    'b'    # s8   NormalizedDrivingLine
    'b'    # s8   NormalizedAIBrakeDifference
)

_FM7_EXPECTED_SIZE = 311


class Fm7Decoder:
    """
    IPacketDecoder implementation for Forza Motorsport 7.
    Handles the "Dash" packet format: 311 bytes, little-endian.

    Registered in PacketDecoderFactory with size key = 311.
    """

    def decode(self, data: bytes, received_at: datetime) -> RawTelemetry:
        """
        Unpacks 311-byte FM7 binary payload into RawTelemetry primitives.

        Raises:
            struct.error — if data is corrupted or truncated.
        """
        fields = struct.unpack_from(_FM7_FORMAT, data)
        return RawTelemetry(
            received_at=received_at,
            IsRaceOn=fields[0],
            TimestampMS=fields[1],
            EngineMaxRpm=fields[2],
            EngineIdleRpm=fields[3],
            CurrentEngineRpm=fields[4],
            AccelerationX=fields[5],
            AccelerationY=fields[6],
            AccelerationZ=fields[7],
            VelocityX=fields[8],
            VelocityY=fields[9],
            VelocityZ=fields[10],
            AngularVelocityX=fields[11],
            AngularVelocityY=fields[12],
            AngularVelocityZ=fields[13],
            Yaw=fields[14],
            Pitch=fields[15],
            Roll=fields[16],
            NormalizedSuspensionTravelFrontLeft=fields[17],
            NormalizedSuspensionTravelFrontRight=fields[18],
            NormalizedSuspensionTravelRearLeft=fields[19],
            NormalizedSuspensionTravelRearRight=fields[20],
            TireSlipRatioFrontLeft=fields[21],
            TireSlipRatioFrontRight=fields[22],
            TireSlipRatioRearLeft=fields[23],
            TireSlipRatioRearRight=fields[24],
            WheelRotationSpeedFrontLeft=fields[25],
            WheelRotationSpeedFrontRight=fields[26],
            WheelRotationSpeedRearLeft=fields[27],
            WheelRotationSpeedRearRight=fields[28],
            WheelOnRumbleStripFrontLeft=fields[29],
            WheelOnRumbleStripFrontRight=fields[30],
            WheelOnRumbleStripRearLeft=fields[31],
            WheelOnRumbleStripRearRight=fields[32],
            WheelInPuddleDepthFrontLeft=fields[33],
            WheelInPuddleDepthFrontRight=fields[34],
            WheelInPuddleDepthRearLeft=fields[35],
            WheelInPuddleDepthRearRight=fields[36],
            SurfaceRumbleFrontLeft=fields[37],
            SurfaceRumbleFrontRight=fields[38],
            SurfaceRumbleRearLeft=fields[39],
            SurfaceRumbleRearRight=fields[40],
            TireSlipAngleFrontLeft=fields[41],
            TireSlipAngleFrontRight=fields[42],
            TireSlipAngleRearLeft=fields[43],
            TireSlipAngleRearRight=fields[44],
            TireCombinedSlipFrontLeft=fields[45],
            TireCombinedSlipFrontRight=fields[46],
            TireCombinedSlipRearLeft=fields[47],
            TireCombinedSlipRearRight=fields[48],
            SuspensionTravelMetersFrontLeft=fields[49],
            SuspensionTravelMetersFrontRight=fields[50],
            SuspensionTravelMetersRearLeft=fields[51],
            SuspensionTravelMetersRearRight=fields[52],
            CarOrdinal=fields[53],
            CarClass=fields[54],
            CarPerformanceIndex=fields[55],
            DrivetrainType=fields[56],
            NumCylinders=fields[57],
            PositionX=fields[58],
            PositionY=fields[59],
            PositionZ=fields[60],
            Speed=fields[61],
            Power=fields[62],
            Torque=fields[63],
            TireTempFrontLeft=fields[64],
            TireTempFrontRight=fields[65],
            TireTempRearLeft=fields[66],
            TireTempRearRight=fields[67],
            Boost=fields[68],
            Fuel=fields[69],
            DistanceTraveled=fields[70],
            BestLap=fields[71],
            LastLap=fields[72],
            CurrentLap=fields[73],
            CurrentRaceTime=fields[74],
            LapNumber=fields[75],
            RacePosition=fields[76],
            Accel=fields[77],
            Brake=fields[78],
            Clutch=fields[79],
            HandBrake=fields[80],
            Gear=fields[81],
            Steer=fields[82],
            NormalizedDrivingLine=fields[83],
            NormalizedAIBrakeDifference=fields[84],
            # FM7 has no extended FH4/FH5 fields
            HorizonPlaceholder=None,
        )
