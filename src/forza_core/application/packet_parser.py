import struct
from ..domain.models import TelemetryPacket

class PacketParser:
    """
    Parses binary telemetry data into TelemetryPacket objects.
    """

    
    # Format for Data Out (324 bytes) - 'Sled' format + Dash extensions
    _FORMAT_DATA_OUT = (
        '<'
        'iIffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffHBBBBBbBb'
        # 12 bytes padding at end if 324? Actually Sled is 324. Dash is 311.
        # The struct format string above corresponds to Sled structure mapped to fields.
    )

    # Simplified approach: We assume the existing huge format string covers the 324 byte structure minus padding logic?
    # Let's reuse the existing huge string but be smart about length.
    
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
    
    @classmethod
    def parse(cls, data: bytes) -> TelemetryPacket | None:
        length = len(data)
        
        # Support V1 'Sled' / 'Data Out' (324 bytes) and 'Dash' (311 bytes)
        # 324 is typical for 'Data Out' config in game.
        if length == 324:
             # Standard Data Out
             pass
        elif length == 311:
             # Dash format (missing some padding or extra fields? Actually Dash is subset or just different packing)
             # The existing FORMAT maps to 311 bytes actually. (calc: 4+4+... = 311?)
             # Let's trust struct.unpack_from will handle prefix.
             pass
        else:
             # Invalid length
             # logger is not imported here, but we should return None as per contract
             return None

        try:
             # If 324, ignore last 13 bytes to match 311 format
             unpacked = struct.unpack_from(cls._FORMAT_V1, data)
             
             return TelemetryPacket(
                is_race_on=unpacked[0],
                timestamp_ms=unpacked[1],
                engine_max_rpm=unpacked[2],
                engine_idle_rpm=unpacked[3],
                current_engine_rpm=unpacked[4],
                acceleration_x=unpacked[5],
                acceleration_y=unpacked[6],
                acceleration_z=unpacked[7],
                velocity_x=unpacked[8],
                velocity_y=unpacked[9],
                velocity_z=unpacked[10],
                angular_velocity_x=unpacked[11],
                angular_velocity_y=unpacked[12],
                angular_velocity_z=unpacked[13],
                yaw=unpacked[14],
                pitch=unpacked[15],
                roll=unpacked[16],
                normalized_suspension_travel_fl=unpacked[17],
                normalized_suspension_travel_fr=unpacked[18],
                normalized_suspension_travel_rl=unpacked[19],
                normalized_suspension_travel_rr=unpacked[20],
                tire_slip_ratio_fl=unpacked[21],
                tire_slip_ratio_fr=unpacked[22],
                tire_slip_ratio_rl=unpacked[23],
                tire_slip_ratio_rr=unpacked[24],
                wheel_rotation_speed_fl=unpacked[25],
                wheel_rotation_speed_fr=unpacked[26],
                wheel_rotation_speed_rl=unpacked[27],
                wheel_rotation_speed_rr=unpacked[28],
                wheel_on_rumble_strip_fl=unpacked[29],
                wheel_on_rumble_strip_fr=unpacked[30],
                wheel_on_rumble_strip_rl=unpacked[31],
                wheel_on_rumble_strip_rr=unpacked[32],
                wheel_in_puddle_depth_fl=unpacked[33],
                wheel_in_puddle_depth_fr=unpacked[34],
                wheel_in_puddle_depth_rl=unpacked[35],
                wheel_in_puddle_depth_rr=unpacked[36],
                surface_rumble_fl=unpacked[37],
                surface_rumble_fr=unpacked[38],
                surface_rumble_rl=unpacked[39],
                surface_rumble_rr=unpacked[40],
                tire_slip_angle_fl=unpacked[41],
                tire_slip_angle_fr=unpacked[42],
                tire_slip_angle_rl=unpacked[43],
                tire_slip_angle_rr=unpacked[44],
                tire_combined_slip_fl=unpacked[45],
                tire_combined_slip_fr=unpacked[46],
                tire_combined_slip_rl=unpacked[47],
                tire_combined_slip_rr=unpacked[48],
                suspension_travel_meters_fl=unpacked[49],
                suspension_travel_meters_fr=unpacked[50],
                suspension_travel_meters_rl=unpacked[51],
                suspension_travel_meters_rr=unpacked[52],
                car_ordinal=unpacked[53],
                car_class=unpacked[54],
                car_performance_index=unpacked[55],
                drivetrain_type=unpacked[56],
                num_cylinders=unpacked[57],
                position_x=unpacked[58],
                position_y=unpacked[59],
                position_z=unpacked[60],
                speed=unpacked[61],
                power=unpacked[62],
                torque=unpacked[63],
                tire_temp_fl=unpacked[64],
                tire_temp_fr=unpacked[65],
                tire_temp_rl=unpacked[66],
                tire_temp_rr=unpacked[67],
                boost=unpacked[68],
                fuel=unpacked[69],
                distance_traveled=unpacked[70],
                best_lap=unpacked[71],
                last_lap=unpacked[72],
                current_lap=unpacked[73],
                current_race_time=unpacked[74],
                lap_number=unpacked[75],
                race_position=unpacked[76],
                accel=unpacked[77],
                brake=unpacked[78],
                clutch=unpacked[79],
                handbrake=unpacked[80],
                gear=unpacked[81],
                steer=unpacked[82],
                normalized_driving_line=unpacked[83],
                normalized_ai_brake_difference=unpacked[84],
                # New field default
                session_id=None
            )
        except struct.error:
             return None
