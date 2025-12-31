import dataclasses

@dataclasses.dataclass(frozen=True)
class RaceStarted:
    """
    Event triggered when the race starts (IsRaceOn transitions from 0 to 1).
    """
    timestamp: float
    car_ordinal: int
    car_class: int
    car_performance_index: int
