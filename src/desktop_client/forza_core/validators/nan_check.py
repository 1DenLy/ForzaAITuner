import math
import dataclasses
from ...domain.models import TelemetryPacket
from ..models import ValidationResult


class NaNCheck:
    """
    IValidationCheck — Step 1 in the Chain of Responsibility.

    Checks all float fields for NaN or Inf values.
    Runs first because NaN/Inf in subsequent checks can cause unintended behavior.
    """

    def check(self, packet: TelemetryPacket) -> ValidationResult:
        """
        Iterates over all float fields and fails on the first NaN or Inf found.
        """
        for field in dataclasses.fields(packet):
            value = getattr(packet, field.name)
            if isinstance(value, float):
                if math.isnan(value):
                    return ValidationResult.fail(f"NaN detected in field '{field.name}'")
                if math.isinf(value):
                    return ValidationResult.fail(f"Inf detected in field '{field.name}'")
        return ValidationResult.ok()
