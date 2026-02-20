import pytest
from unittest.mock import MagicMock
from forza_core.application.race_monitor import RaceStateMonitor
from forza_core.domain.events import RaceStarted
from forza_core.domain.models import TelemetryPacket

@pytest.fixture
def monitor():
    return RaceStateMonitor()

def create_mock_packet(is_race_on: int) -> TelemetryPacket:
    packet = MagicMock(spec=TelemetryPacket)
    packet.is_race_on = is_race_on
    packet.current_race_time = 123.45
    packet.car_ordinal = 1
    packet.car_class = 2
    packet.car_performance_index = 800
    return packet

def test_race_starts_emits_event(monitor):
    packet = create_mock_packet(is_race_on=1)
    events = monitor.detect_events(packet)
    
    assert len(events) == 1
    assert isinstance(events[0], RaceStarted)

def test_race_stays_on_no_new_events(monitor):
    packet1 = create_mock_packet(is_race_on=1)
    packet2 = create_mock_packet(is_race_on=1)
    
    monitor.detect_events(packet1)
    
    events = monitor.detect_events(packet2)
    assert len(events) == 0