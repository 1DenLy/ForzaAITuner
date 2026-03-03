"""
Tests for ValidationResult — Generic Result-паттерн.
"""

import pytest
from desktop_client.application.validation_result import ValidationResult


class TestValidationResultSuccess:
    def test_success_factory_sets_is_valid_true(self):
        result = ValidationResult.success(data={"key": "value"})
        assert result.is_valid is True

    def test_success_factory_stores_data(self):
        payload = {"answer": 42}
        result = ValidationResult.success(data=payload)
        assert result.data == payload

    def test_success_factory_errors_are_empty(self):
        result = ValidationResult.success(data="anything")
        assert result.errors == {}


class TestValidationResultFailure:
    def test_failure_factory_sets_is_valid_false(self):
        result = ValidationResult.failure(errors={"field": "bad value"})
        assert result.is_valid is False

    def test_failure_factory_stores_errors(self):
        errors = {"tires -> front_pressure_bar": "value is not a valid float"}
        result = ValidationResult.failure(errors=errors)
        assert result.errors == errors

    def test_failure_factory_data_is_none(self):
        result = ValidationResult.failure(errors={"x": "err"})
        assert result.data is None


class TestValidationResultImmutability:
    def test_result_is_frozen(self):
        result = ValidationResult.success(data=42)
        with pytest.raises((AttributeError, TypeError)):
            result.is_valid = False  # type: ignore[misc]

    def test_default_errors_do_not_share_state(self):
        """Each instance should have its own errors dict (not shared via default_factory)."""
        r1 = ValidationResult(is_valid=False, errors={"a": "1"})
        r2 = ValidationResult(is_valid=False, errors={})
        assert r1.errors is not r2.errors
