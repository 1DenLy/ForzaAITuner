import struct
import structlog
from typing import Tuple, Any
from ...domain.interface.i_packet_decoder import IPacketDecoder

logger = structlog.get_logger()

class PacketDecoder(IPacketDecoder):
    """
    Decodes binary telemetry data into raw tuples using struct.
    """

    # Format for 'Dash' (311 bytes) and 'Sled+' (324 bytes) versions.
    _FORMAT_V1 = (
        '<'
        'i'  # s32 IsRaceOn
        'I'  # u32 TimestampMS
        'f'  # f32 EngineMaxRpm
        'f'  # f32 EngineIdleRpm
        'f'  # f32 CurrentEngineRpm
        'fff'  # Acceleration X, Y, Z
        'fff'  # Velocity X, Y, Z
        'fff'  # AngularVelocity X, Y, Z
        'fff'  # Yaw, Pitch, Roll
        'ffff' # NormSuspTravel FL, FR, RL, RR
        'ffff' # TireSlipRatio FL, FR, RL, RR
        'ffff' # WheelRotSpeed FL, FR, RL, RR
        'iiii' # WheelOnRumble FL, FR, RL, RR (s32)
        'ffff' # WheelInPuddle FL, FR, RL, RR
        'ffff' # SurfaceRumble FL, FR, RL, RR
        'ffff' # TireSlipAngle FL, FR, RL, RR
        'ffff' # TireCombSlip FL, FR, RL, RR
        'ffff' # SuspTravelMeters FL, FR, RL, RR
        'i'    # s32 CarOrdinal
        'i'    # s32 CarClass
        'i'    # s32 CarPerfIndex
        'i'    # s32 DrivetrainType
        'i'    # s32 NumCylinders
        'fff'  # Position X, Y, Z
        'f'    # Speed
        'f'    # Power
        'f'    # Torque
        'ffff' # TireTemp FL, FR, RL, RR
        'f'    # Boost
        'f'    # Fuel
        'f'    # DistTraveled
        'f'    # BestLap
        'f'    # LastLap
        'f'    # CurLap
        'f'    # CurRaceTime
        'H'    # u16 LapNo
        'B'    # u8 RacePos
        'B'    # u8 Accel
        'B'    # u8 Brake
        'B'    # u8 Clutch
        'B'    # u8 HandBrake
        'B'    # u8 Gear
        'b'    # s8 Steer
        'b'    # s8 DriLine
        'b'    # s8 AIBrakeDiff
    )

    def decode(self, data: bytes) -> Tuple[Any, ...] | None:
        try:
             return struct.unpack_from(self._FORMAT_V1, data)
        except struct.error as e:
             logger.error("packet_decoder_binary_error", error=str(e), packet_size=len(data))
             return None
        except Exception as e:
             logger.error("packet_decoder_unexpected_error", error=str(e))
             return None
