# Car Configuration Pydantic Model

This document defines the Pydantic model for the car configuration data used

## Pydantic Model Implementation

```python
class CarConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

class Session(BaseModel):
    name: str = Field(alias="Name")
    car: str = Field(alias="Car")
    pi_rating: int
    road_type: str = Field(alias="Road_Type")
    location: str = Field(alias="Location")
    surface: str = Field(alias="Surface")

class Info(BaseModel):
    weight_kg: int
    weight_dist_front: int
    power_hp: int
    torque_nm: int
    suspension_travel: int
    engine_location: EngineLocation
    drive_type: DrivetrainType
    engine_placement: EngineLocation = Field(alias="Engine_placement")

class Tires(BaseModel):
    pressure_front: float
    pressure_rear: float
    width_front: int
    width_rear: int
    compound: str

class Alignment(BaseModel):
    camber_front: float
    camber_rear: float
    toe_front: float
    toe_rear: float
    caster: float

class Spring(BaseModel):
    spring_front: float
    spring_rear: float
    clearance_front: float
    clearance_rear: float
    spring_front_min: float
    spring_front_max: float
    spring_rear_min: float
    spring_rear_max: float
    clearance_front_min: float
    clearance_front_max: float
    clearance_rear_min: float
    clearance_rear_max: float

class Damping(BaseModel):
    rebound_front: float
    rebound_rear: float
    bump_front: float
    bump_rear: float
    rebound_front_min: float
    rebound_front_max: float
    rebound_rear_min: float
    rebound_rear_max: float
    bump_front_min: float
    bump_front_max: float
    bump_rear_min: float
    bump_rear_max: float

class RollBar(BaseModel):
    roll_bar_front: float
    roll_bar_rear: float

class Aero(BaseModel):
    has_adjustable_aero_front: bool
    has_adjustable_aero_rear: bool
    front: int
    rear: int
    front_min: int
    front_max: int
    rear_min: int
    rear_max: int

class Brakes(BaseModel):
    balance: float
    power: int

class Differential(BaseModel):
    front_acceleration: int
    front_deceleration: int
    rear_acceleration: int
    rear_deceleration: int
    balance: int

class CarConfig(BaseModel):
    session: Session = Field(alias="Session")
    info: Info = Field(alias="Info")
    tires: Tires = Field(alias="Tires")
    alignment: Alignment = Field(alias="Alignment")
    spring: Spring = Field(alias="Spring")
    damping: Damping = Field(alias="Damping")
    roll_bar: RollBar = Field(alias="Roll-Bar")
    aero: Aero = Field(alias="Aero")
    brakes: Brakes = Field(alias="Brakes")
    differential: Differential = Field(alias="Deffrential")

```

## Enums list
```python
class DrivetrainType(enum.Enum):
    RWD = "RWD"
    FWD = "FWD"
    AWD = "AWD"

class EngineLocation(enum.Enum):
    Front = "Front"
    Mid = "Mid"
    Rear = "Rear"

class CarClass(enum.Enum):
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S1 = "S1"
    S2 = "S2"
    X = "X"
```