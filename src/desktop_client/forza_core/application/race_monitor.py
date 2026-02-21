from typing import List, Optional
import dataclasses
from ..domain.models import TelemetryPacket
from ..domain.events import RaceStarted, RaceStopped

class RaceStateMonitor:
    """
    Monitors race state transitions (Started/Stopped).
    SRP: Handles only state detection logic.
    """
    def __init__(self):
        self._last_is_race_on = 0

    def detect_events(self, packet: TelemetryPacket) -> List:
        """
        Check for state transitions based on current packet.
        Returns a list of domain events (e.g. RaceStarted).
        """
        events = []
        
        # State Machine: IsRaceOn 0 -> 1 (Race Started)
        if self._last_is_race_on == 0 and packet.is_race_on == 1:
            events.append(RaceStarted(
                timestamp=packet.current_race_time,
                car_ordinal=packet.car_ordinal,
                car_class=packet.car_class,
                car_performance_index=packet.car_performance_index
            ))
            
        # State Machine: IsRaceOn 1 -> 0 (Race Ended)
        if self._last_is_race_on == 1 and packet.is_race_on == 0:
            events.append(RaceStopped(
                timestamp=packet.current_race_time
            ))
        
        self._last_is_race_on = packet.is_race_on
        return events
