import dataclasses
from .models import ValidationResult, ValidationError, ValidationErrorCode
from typing import Any, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from desktop_client.domain.models.telemetry_models import TelemetryPacket

class PacketValidator:
    """
    Validator for incoming UDP telemetry packets.
    Checks data type and packet length against known Forza formats.
    
    Supported sizes:
    - 232 (Sled - FH3/FM6/FM7)
    - 311 (Dash - FH4/FH5)
    - 324 (Sled+ - FH4/FH5)
    """
    
    DEFAULT_ALLOWED_SIZES = {232, 311, 324}

    def __init__(self, allowed_sizes: set[int] = None):
        self._allowed_sizes = allowed_sizes if allowed_sizes is not None else self.DEFAULT_ALLOWED_SIZES
    
    def validate(self, data: Any) -> ValidationResult[bytes]:
        if not isinstance(data, bytes):
            return ValidationResult(
                is_valid=False,
                errors=(ValidationError(ValidationErrorCode.INVALID_TYPE, f"Expected bytes, got {type(data).__name__}"),)
            )
            
        length = len(data)
        if length not in self._allowed_sizes:
            return ValidationResult(
                is_valid=False,
                errors=(ValidationError(ValidationErrorCode.INVALID_LENGTH, f"Incorrect packet size: {length} bytes."),)
            )
            
        return ValidationResult(is_valid=True, data=data)

class TelemetrySanityValidator:
    """
    Checks the physical correctness of telemetry data (Sanity Check).
    Protects against NaN and Infinity which can cause UI and logic crashes.
    """
    
    def validate(self, data: "TelemetryPacket") -> ValidationResult["TelemetryPacket"]:
        """
        Checks all float fields of the packet for finiteness (neither NaN nor Infinity).
        """
        if not dataclasses.is_dataclass(data):
            return ValidationResult(
                is_valid=False,
                errors=(ValidationError(
                    ValidationErrorCode.NOT_A_DATACLASS, 
                    f"Expected dataclass, got {type(data).__name__}"
                ),)
            )

        for field in dataclasses.fields(data):
            value = getattr(data, field.name)
            if isinstance(value, float) and not math.isfinite(value):
                return ValidationResult(
                    is_valid=False,
                    errors=(ValidationError(
                        ValidationErrorCode.INVALID_FLOAT, 
                        f"Field '{field.name}' contains invalid value: {value}", 
                        location=field.name
                    ),)
                )
        return ValidationResult(is_valid=True, data=data)
