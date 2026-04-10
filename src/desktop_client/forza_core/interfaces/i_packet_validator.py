from typing import Protocol
from ...domain.models import TelemetryPacket
from ..models import ValidationResult


class IPacketValidator(Protocol):
    """
    Domain interface for full telemetry validation.

    Implements Chain of Responsibility: Sanity Check → Range Check → Consistency Check.
    This is the ONLY component that decides whether a TelemetryPacket is accepted or rejected.

    The parser (IPacketParser) may produce packets with NaN values — the validator filters them.
    """

    def validate(self, packet: TelemetryPacket) -> ValidationResult:
        """
        Runs the full validation chain.

        Returns:
            ValidationResult(is_valid=True)            — packet is accepted.
            ValidationResult(is_valid=False, reason=…) — packet is rejected with reason.
        Does NOT raise exceptions. All failure cases are encoded in ValidationResult.
        """
        ...
