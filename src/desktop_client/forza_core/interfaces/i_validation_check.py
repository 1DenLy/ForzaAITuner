from typing import Protocol
from ...domain.models import TelemetryPacket
from ..models import ValidationResult


class IValidationCheck(Protocol):
    """
    Single validation step in the Chain of Responsibility.

    Implementations: NaNCheck, RangeCheck, ConsistencyCheck.
    New checks are added as new IValidationCheck classes without modifying
    TelemetrySanityValidator (Open/Closed Principle).
    """

    def check(self, packet: TelemetryPacket) -> ValidationResult:
        """
        Performs a specific validation check on the packet.

        Returns:
            ValidationResult.ok()         — check passed.
            ValidationResult.fail(reason) — check failed with reason.
        """
        ...
