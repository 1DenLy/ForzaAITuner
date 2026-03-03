"""
Tests for ConfigValidatorService — Generic Application-layer validator.

Covers:
  - Happy path (valid data → ValidationResult.is_valid=True, data populated)
  - Validation errors (invalid data → ValidationResult.is_valid=False, errors populated)
  - Contract violation (non-dict input → TypeError propagated)
  - Error message safety (no stack traces / system paths in errors dict)
  - Annotated gears validation in Gearing model
  - Unit-suffixed field validation in Suspension model
"""

import pytest
from pydantic import BaseModel, ConfigDict, Field

from desktop_client.application.config_validator_service import ConfigValidatorService
from desktop_client.application.validation_result import ValidationResult
from desktop_client.domain.tuning import (
    Gearing,
    Suspension,
    TuningSetup,
)


# ---------------------------------------------------------------------------
# Minimal stub model for isolated unit tests
# ---------------------------------------------------------------------------

class _SimpleModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    name: str
    value: float = Field(gt=0)


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

class TestConfigValidatorServiceHappyPath:
    def test_valid_simple_model_returns_success(self):
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"name": "test", "value": 3.14})

        assert result.is_valid is True
        assert isinstance(result.data, _SimpleModel)
        assert result.data.name == "test"
        assert result.data.value == pytest.approx(3.14)

    def test_valid_result_has_empty_errors(self):
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"name": "ok", "value": 1.0})
        assert result.errors == {}

    def test_returns_validation_result_instance(self):
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"name": "x", "value": 0.1})
        assert isinstance(result, ValidationResult)


# ---------------------------------------------------------------------------
# Validation errors
# ---------------------------------------------------------------------------

class TestConfigValidatorServiceValidationErrors:
    def test_invalid_data_returns_failure(self):
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"name": "test", "value": -5.0})  # value must be > 0

        assert result.is_valid is False
        assert result.data is None

    def test_errors_dict_is_non_empty_on_failure(self):
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"name": "test", "value": -5.0})
        assert len(result.errors) > 0

    def test_missing_required_field_captured(self):
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"name": "test"})  # value is missing

        assert result.is_valid is False
        # Should have an error entry referencing "value"
        assert any("value" in k for k in result.errors)

    def test_extra_field_forbidden(self):
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"name": "test", "value": 1.0, "unknown_field": True})

        assert result.is_valid is False

    def test_error_values_are_strings(self):
        """Ошибки должны быть строками, безопасными для отображения в UI."""
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"value": 0})  # name missing, value=0 violates gt=0
        for key, msg in result.errors.items():
            assert isinstance(key, str), f"Key {key!r} is not a str"
            assert isinstance(msg, str), f"Message {msg!r} is not a str"

    def test_error_values_contain_no_stack_trace(self):
        """Никаких Traceback или File path в ошибках для UI."""
        svc = ConfigValidatorService(_SimpleModel)
        result = svc.validate({"name": 123, "value": -1})
        for msg in result.errors.values():
            assert "Traceback" not in msg
            assert "File " not in msg


# ---------------------------------------------------------------------------
# Contract violations (TypeError must propagate)
# ---------------------------------------------------------------------------

class TestConfigValidatorServiceContractViolations:
    def test_list_input_raises_type_error(self):
        svc = ConfigValidatorService(_SimpleModel)
        with pytest.raises(TypeError):
            svc.validate(["not", "a", "dict"])  # type: ignore[arg-type]

    def test_string_input_raises_type_error(self):
        svc = ConfigValidatorService(_SimpleModel)
        with pytest.raises(TypeError):
            svc.validate('{"name": "test", "value": 1.0}')  # type: ignore[arg-type]

    def test_none_input_raises_type_error(self):
        svc = ConfigValidatorService(_SimpleModel)
        with pytest.raises(TypeError):
            svc.validate(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Gearing — Annotated gears validation
# ---------------------------------------------------------------------------

class TestGearingAnnotatedValidation:
    def _svc(self) -> ConfigValidatorService[Gearing]:
        return ConfigValidatorService(Gearing)

    def test_valid_gearing_passes(self):
        raw = {"final_drive": 3.5, "gears": [2.9, 1.9, 1.3, 1.0, 0.8, 0.6]}
        result = self._svc().validate(raw)
        assert result.is_valid is True
        assert result.data is not None
        assert len(result.data.gears) == 6

    @pytest.mark.parametrize(
        "invalid_raw",
        [
            pytest.param({"final_drive": 3.5, "gears": []}, id="empty list"),
            pytest.param({"final_drive": 3.5, "gears": [2.5, 0.0, 1.0]}, id="zero gear ratio"),
            pytest.param({"final_drive": 3.5, "gears": [2.5, -1.0]}, id="negative gear ratio"),
            pytest.param({"final_drive": -1.0, "gears": [2.0]}, id="negative final drive"),
        ],
    )
    def test_invalid_gearing_fails(self, invalid_raw):
        result = self._svc().validate(invalid_raw)
        assert result.is_valid is False

    def test_single_gear_passes(self):
        raw = {"final_drive": 4.0, "gears": [3.0]}
        result = self._svc().validate(raw)
        assert result.is_valid is True


# ---------------------------------------------------------------------------
# Suspension — unit-suffixed fields
# ---------------------------------------------------------------------------

class TestSuspensionUnitSuffixValidation:
    def _svc(self) -> ConfigValidatorService[Suspension]:
        return ConfigValidatorService(Suspension)

    def test_valid_suspension_passes(self):
        raw = {
            "spring_front": 160.0,
            "spring_rear": 220.0,
            "spring_min": 50.0,
            "spring_max": 250.0,
            "clearance_front": 12.1,
            "clearance_rear": 13.8,
            "clearance_min": 10.0,
            "clearance_max": 20.0,
        }
        result = self._svc().validate(raw)
        assert result.is_valid is True

    def test_missing_field_fails(self):
        raw = {
            "spring_front": 160.0,
            "spring_rear": 220.0,
            # missing spring_min, spring_max, etc.
            "clearance_front": 12.1,
        }
        result = self._svc().validate(raw)
        assert result.is_valid is False
        assert any("spring_min" in k for k in result.errors)

    def test_invalid_type_fails(self):
        raw = {
            "spring_front": 160.0,
            "spring_rear": 220.0,
            "spring_min": 50.0,
            "spring_max": 250.0,
            "clearance_front": "not a number",  # invalid
            "clearance_rear": 13.8,
            "clearance_min": 10.0,
            "clearance_max": 20.0,
        }
        result = self._svc().validate(raw)
        assert result.is_valid is False

