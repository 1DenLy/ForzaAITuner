import struct
import structlog
from ...domain.models import TelemetryPacket
from ...domain.interface.interfaces import IPacketParser

logger = structlog.get_logger()

class PacketParser(IPacketParser):
    """
    Parses binary telemetry data into TelemetryPacket objects.
    
    Responsibilities:
    - Decoding binary Forza format (struct unpack).
    - Mapping data to domain DTO (TelemetryPacket).
    """

    # Format for 'Dash' (311 bytes) and 'Sled+' (324 bytes) versions.
    # Note: 324 bytes version just has extra data at the end which we ignore.
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
    
    def parse(self, data: bytes) -> TelemetryPacket | None:
        """
        Parses bytes into TelemetryPacket.
        Assumes data has been pre-validated for length.
        """
        try:
             # Unpack the fixed part of the packet.
             # Using unpack_from allows us to handle both 311 and 324 byte packets 
             # by only reading the first 311 bytes.
             unpacked = struct.unpack_from(self._FORMAT_V1, data)
             
             # Professional approach: use tuple unpacking as the field order 
             # in TelemetryPacket matches the binary protocol order exactly.
             return TelemetryPacket(*unpacked, session_id=None)
             
        except struct.error as e:
             logger.error("packet_parser_binary_error", error=str(e), packet_size=len(data))
             return None
        except Exception as e:
             logger.error("packet_parser_unexpected_error", error=str(e))
             return None
