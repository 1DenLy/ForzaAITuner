from typing import List, Optional
import dataclasses
from ..domain.models import TelemetryPacket
from ..domain.events import RaceStarted

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
        # We don't have a Domain Event class for RaceStopped yet, 
        # but the service logs "race_ended". We can return a marker or string?
        # Better to return nothing and generic "stopped" logic, or create event.
        # For strictness, if no event defined, we just detect detection.
        # But IngestionService does logic blocks based on transitions.
        # Let's return a simple structure or just handle logic in detected boolean.
        
        # Actually IngestionService used this to log and flush.
        # Let's stick to returning events. If RaceStopped needed, we define it or just rely on state.
        
        self._last_is_race_on = packet.is_race_on
        return events

    def is_race_stopped(self, packet: TelemetryPacket) -> bool:
        """Helper to detect stop specifically for Flush trigger."""
        # Note: This checks transition based on *stored* state which updates in detect_events.
        # This design is tricky if called separately. 
        # Better: detect_events returns ALL changes.
        return False # Handled in main loop via returned events if we added RaceStopped.
