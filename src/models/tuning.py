from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class BaseTuningModel(BaseModel):
    """Base immutable model for tuning configurations."""
    model_config = ConfigDict(frozen=True, extra="forbid")

class Tires(BaseTuningModel):
    """Tire pressure settings."""
    front_pressure_bar: float = Field(
        ...,
        ge=0.5,
        le=5.0,
        description="Front tire pressure (Bar). Range: 0.5 - 5.0."
    )
    rear_pressure_bar: float = Field(
        ...,
        ge=0.5,
        le=5.0,
        description="Rear tire pressure (Bar). Range: 0.5 - 5.0."
    )

class Gearing(BaseTuningModel):
    """Transmission and gearing settings."""
    final_drive: float = Field(
        ...,
        gt=0,
        description="Final drive ratio. Must be > 0."
    )
    gears: list[float] = Field(
        ...,
        min_length=1,
        description="Gear ratios (1st, 2nd, ...). All > 0."
    )

    @field_validator('gears')
    @classmethod
    def check_gears_positive(cls, v: list[float]) -> list[float]:
        """Ensure all gear ratios are positive."""
        if any(g <= 0 for g in v):
            raise ValueError("All gear ratios must be > 0.")
        return v

class Alignment(BaseTuningModel):
    """Wheel alignment settings."""
    camber_front_deg: float = Field(
        ...,
        ge=-7.0,
        le=7.0,
        description="Front camber (deg). Range: -7.0 to +7.0."
    )
    camber_rear_deg: float = Field(
        ...,
        ge=-7.0,
        le=7.0,
        description="Rear camber (deg). Range: -7.0 to +7.0."
    )
    toe_front_deg: float = Field(
        ...,
        ge=-5.0,
        le=5.0,
        description="Front toe (deg). Range: -5.0 to +5.0."
    )
    toe_rear_deg: float = Field(
        ...,
        ge=-5.0,
        le=5.0,
        description="Rear toe (deg). Range: -5.0 to +5.0."
    )
    caster_deg: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Caster angle (deg). Range: 0.0 to 10.0."
    )

class Suspension(BaseTuningModel):
    """Suspension settings (Springs, Ride Height)."""
    spring_rate_front_kgf_mm: float = Field(
        ...,
        gt=0,
        description="Front spring rate (kgf/mm). Must be > 0."
    )
    spring_rate_rear_kgf_mm: float = Field(
        ...,
        gt=0,
        description="Rear spring rate (kgf/mm). Must be > 0."
    )
    ride_height_front_cm: float = Field(
        ...,
        gt=0,
        description="Front ride height (cm). Must be > 0."
    )
    ride_height_rear_cm: float = Field(
        ...,
        gt=0,
        description="Rear ride height (cm). Must be > 0."
    )

class Damping(BaseTuningModel):
    """Damper settings (Bump/Rebound)."""
    rebound_front: float = Field(
        ...,
        ge=1.0,
        le=20.0,
        description="Front rebound stiffness. Range: 1.0 - 20.0."
    )
    rebound_rear: float = Field(
        ...,
        ge=1.0,
        le=20.0,
        description="Rear rebound stiffness. Range: 1.0 - 20.0."
    )
    bump_front: float = Field(
        ...,
        ge=1.0,
        le=20.0,
        description="Front bump stiffness. Range: 1.0 - 20.0."
    )
    bump_rear: float = Field(
        ...,
        ge=1.0,
        le=20.0,
        description="Rear bump stiffness. Range: 1.0 - 20.0."
    )

class Brakes(BaseTuningModel):
    """Brake system settings."""
    balance_front_pct: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Front brake bias (%). Range: 0 - 100."
    )
    pressure_pct: float = Field(
        ...,
        ge=0.0,
        le=200.0,
        description="Brake pressure (%). Range: 0 - 200."
    )

class Differential(BaseTuningModel):
    """Differential settings."""
    accel_lock_front_pct: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Front accel lock (%). Optional."
    )
    decel_lock_front_pct: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Front decel lock (%). Optional."
    )
    accel_lock_rear_pct: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Rear accel lock (%). Optional."
    )
    decel_lock_rear_pct: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Rear decel lock (%). Optional."
    )
    center_balance_rear_pct: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="AWD center balance (to rear) (%). Range: 0 - 100."
    )

class Aerodynamics(BaseTuningModel):
    """Aerodynamics settings (Downforce)."""
    downforce_front_kgf: Optional[float] = Field(
        None,
        ge=0.0,
        description="Front downforce (kgf/N). >= 0."
    )
    downforce_rear_kgf: Optional[float] = Field(
        None,
        ge=0.0,
        description="Rear downforce (kgf/N). >= 0."
    )

class TuningSetup(BaseTuningModel):
    """
    Complete static vehicle tuning configuration.
    Composed of all subsystems.
    """
    tires: Tires = Field(..., description="Tire settings")
    gearing: Gearing = Field(..., description="Gearing settings")
    alignment: Alignment = Field(..., description="Wheel alignment")
    suspension: Suspension = Field(..., description="Suspension settings")
    damping: Damping = Field(..., description="Damping settings")
    brakes: Brakes = Field(..., description="Brake settings")
    differential: Differential = Field(..., description="Differential settings")
    aerodynamics: Aerodynamics = Field(..., description="Aerodynamics settings")
