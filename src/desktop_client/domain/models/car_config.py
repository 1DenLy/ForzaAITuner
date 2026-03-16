from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict

class BaseTuningModel(BaseModel):
    """Base immutable model for tuning configurations."""
    model_config = ConfigDict(frozen=True, extra="ignore")

class Session(BaseTuningModel):
    """Session configuration."""
    name: str = Field(..., description="Session name")
    car: str = Field(..., description="Car name")
    class_pi: int = Field(..., ge=100, le=999, description="Car class/PI score")
    road_type: str = Field(..., description="Road type (e.g., Road, Dirt)")
    location: str = Field(..., description="Location: Race against opponents, Open Horizon World, or Time Trial (empty track)")
    surface: str = Field(..., description="Surface condition: Dry, Wet, or Snow/Ice")

class CarInfo(BaseTuningModel):
    """Basic car info/specs."""
    weight: int = Field(..., ge=1, description="Weight of the car (kg/lbs)")
    power: int = Field(..., ge=1, description="Power of the car (HP/kW)")
    torque: int = Field(..., ge=1, description="Torque of the car (Nm/ft-lb)")
    front_weight: float = Field(..., ge=0.0, le=100.0, description="Front weight percentage")
    suspension_travel: int = Field(..., ge=1, description="Suspension travel in mm (e.g., 80, 120)")
    drive_type: str = Field(..., description="Drive type (e.g., AWD, RWD)")
    engine_placement: str = Field(..., description="Engine placement (e.g., Front, Mid)")

class Tires(BaseTuningModel):
    """Tire settings."""
    front_pressure_bar: float = Field(..., ge=1.0, le=3.8, description="Front tire pressure (Bar)")
    rear_pressure_bar: float = Field(..., ge=1.0, le=3.8, description="Rear tire pressure (Bar)")
    width_front: int = Field(..., ge=1, description="Front tire width (mm)")
    width_rear: int = Field(..., ge=1, description="Rear tire width (mm)")
    compound: str = Field(..., description="Tire compound type")

# Annotated Type for gears
GearRatio = Annotated[float, Field(ge=0.1)]

class Gearing(BaseTuningModel):
    """Transmission and gearing settings."""
    final_drive: float = Field(..., ge=0.1, description="Final drive ratio")
    gears: list[GearRatio] = Field(..., min_length=1, description="Gear ratios (1st, 2nd, ...)")

# Default Gearing used when no UI widgets collect gear data yet.
DEFAULT_GEARING = Gearing(final_drive=0.1, gears=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

class Alignment(BaseTuningModel):
    """Wheel alignment settings."""
    camber_front_deg: float = Field(..., ge=-5.0, le=5.0, description="Front camber")
    camber_rear_deg: float = Field(..., ge=-5.0, le=5.0, description="Rear camber")
    toe_front_deg: float = Field(..., ge=-5.0, le=5.0, description="Front toe")
    toe_rear_deg: float = Field(..., ge=-5.0, le=5.0, description="Rear toe")
    caster_front_deg: float = Field(..., ge=1.0, le=7.0, description="Front caster angle")

class AntiRollBars(BaseTuningModel):
    """Anti-roll bar settings."""
    front: float = Field(..., ge=1.0, le=65.0, description="Front anti-roll bar")
    rear: float = Field(..., ge=1.0, le=65.0, description="Rear anti-roll bar")

class Suspension(BaseTuningModel):
    """Suspension settings (Springs, Ride Height)."""
    spring_front: float = Field(..., ge=0.1, description="Front spring rate")
    spring_rear: float = Field(..., ge=0.1, description="Rear spring rate")
    spring_min: float = Field(..., ge=0.1, description="Minimum spring rate allowed")
    spring_max: float = Field(..., ge=0.1, description="Maximum spring rate allowed")
    
    clearance_front: float = Field(..., ge=0.1, description="Front ride height/clearance")
    clearance_rear: float = Field(..., ge=0.1, description="Rear ride height/clearance")
    clearance_min: float = Field(..., ge=0.1, description="Minimum clearance allowed")
    clearance_max: float = Field(..., ge=0.1, description="Maximum clearance allowed")

class Damping(BaseTuningModel):
    """Damper settings (Bump/Rebound)."""
    rebound_front: float = Field(..., ge=1.0, le=20.0, description="Front rebound")
    rebound_rear: float = Field(..., ge=1.0, le=20.0, description="Rear rebound")
    rebound_min: float = Field(..., ge=1.0, le=20.0, description="Min rebound")
    rebound_max: float = Field(..., ge=1.0, le=20.0, description="Max rebound")

    bump_front: float = Field(..., ge=1.0, le=20.0, description="Front bump")
    bump_rear: float = Field(..., ge=1.0, le=20.0, description="Rear bump")
    bump_min: float = Field(..., ge=1.0, le=20.0, description="Min bump")
    bump_max: float = Field(..., ge=1.0, le=20.0, description="Max bump")

class Aerodynamics(BaseTuningModel):
    """Aerodynamics settings (Downforce)."""
    front_enabled: bool = Field(..., description="Is front aero tunable")
    rear_enabled: bool = Field(..., description="Is rear aero tunable")
    
    front: float = Field(..., ge=1.0, description="Front downforce")
    front_min: float = Field(..., ge=1.0, description="Front downforce min")
    front_max: float = Field(..., ge=1.0, description="Front downforce max")
    
    rear: float = Field(..., ge=1.0, description="Rear downforce")
    rear_min: float = Field(..., ge=1.0, description="Rear downforce min")
    rear_max: float = Field(..., ge=1.0, description="Rear downforce max")

class Brakes(BaseTuningModel):
    """Brake system settings."""
    balance_pct: float = Field(..., ge=0.0, le=100.0, description="Front brake bias (%)")
    power_pct: float = Field(..., ge=0.0, le=200.0, description="Brake pressure (%)")

class Differential(BaseTuningModel):
    """Differential settings."""
    acceleration_front: float = Field(..., ge=0.0, le=100.0, description="Front accel lock (%)")
    deceleration_front: float = Field(..., ge=0.0, le=100.0, description="Front decel lock (%)")
    acceleration_rear: float = Field(..., ge=0.0, le=100.0, description="Rear accel lock (%)")
    deceleration_rear: float = Field(..., ge=0.0, le=100.0, description="Rear decel lock (%)")
    balance: float = Field(..., ge=0.0, le=100.0, description="AWD center balance (to rear) (%)")

class Assists(BaseTuningModel):
    """Driving assists settings."""
    abs: bool = Field(..., description="ABS enabled (True/False)")
    stm: bool = Field(..., description="STM enabled (True/False)")
    tcs: bool = Field(..., description="TCS enabled (True/False)")
    shifting: str = Field(..., description="Shifting setting")
    steering: str = Field(..., description="Steering setting")

class CarConfig(BaseTuningModel):
    """
    Complete static vehicle tuning configuration.
    (Formerly TuningSetup)
    """
    session: Session = Field(..., description="Session settings")
    info: CarInfo = Field(..., description="Car specifications")
    tires: Tires = Field(..., description="Tire settings")
    gearing: Gearing = Field(default=DEFAULT_GEARING, description="Gearing settings")
    alignment: Alignment = Field(..., description="Wheel alignment")
    anti_roll_bars: AntiRollBars = Field(..., description="Anti-roll bars")
    suspension: Suspension = Field(..., description="Suspension settings")
    damping: Damping = Field(..., description="Damping settings")
    aerodynamics: Aerodynamics = Field(..., description="Aerodynamics settings")
    brakes: Brakes = Field(..., description="Brake settings")
    differential: Differential = Field(..., description="Differential settings")
    assists: Assists = Field(..., description="Driving assists")
