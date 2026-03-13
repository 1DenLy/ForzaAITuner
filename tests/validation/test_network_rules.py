import pytest
from desktop_client.validation.network_rules import PacketValidator, TelemetrySanityValidator
from desktop_client.validation.models import ValidationResult
import dataclasses
from typing import Optional

@dataclasses.dataclass
class MockTelemetryPacket:
    speed: float = 0.0
    rpm: float = 0.0
    is_race_on: int = 0

def test_packet_validator_default_sizes():
    validator = PacketValidator()
    # Test valid sizes
    assert validator.validate(b" " * 232).is_valid
    assert validator.validate(b" " * 311).is_valid
    assert validator.validate(b" " * 324).is_valid
    
    # Test invalid size
    res = validator.validate(b" " * 100)
    assert not res.is_valid
    assert res.errors[0].code == "invalid_length"

def test_packet_validator_custom_sizes():
    validator = PacketValidator(allowed_sizes={100, 200})
    assert validator.validate(b" " * 100).is_valid
    assert validator.validate(b" " * 200).is_valid
    assert not validator.validate(b" " * 232).is_valid

def test_telemetry_sanity_validator_valid():
    validator = TelemetrySanityValidator()
    packet = MockTelemetryPacket(speed=100.5, rpm=5000.0)
    res = validator.validate(packet)
    assert res.is_valid
    assert res.data == packet

def test_telemetry_sanity_validator_nan():
    validator = TelemetrySanityValidator()
    packet = MockTelemetryPacket(speed=float('nan'), rpm=5000.0)
    res = validator.validate(packet)
    assert not res.is_valid
    assert res.errors[0].code == "invalid_float"
    assert "speed" in res.errors[0].message

def test_telemetry_sanity_validator_inf():
    validator = TelemetrySanityValidator()
    packet = MockTelemetryPacket(speed=100.5, rpm=float('inf'))
    res = validator.validate(packet)
    assert not res.is_valid
    assert res.errors[0].code == "invalid_float"
    assert "rpm" in res.errors[0].message
