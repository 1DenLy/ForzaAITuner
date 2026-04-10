from ..interfaces import IValidationCheck
from ...domain.models import TelemetryPacket
from ..models import ValidationResult


class TelemetrySanityValidator:
    """
    IPacketValidator implementation using Chain of Responsibility.

    Runs validation checks in order: NaNCheck → RangeCheck → ConsistencyCheck.
    Stops at the first failure and returns ValidationResult(is_valid=False, reason=…).
    Returns ValidationResult.ok() only if all checks pass.

    New checks are added as new IValidationCheck implementations registered in
    the constructor — no modification of this class required (OCP).

    Usage (Composition Root):
        validator = TelemetrySanityValidator(checks=[
            NaNCheck(),
            RangeCheck(),
            ConsistencyCheck(),
        ])
    """

    def __init__(self, checks: list[IValidationCheck]) -> None:
        self._checks = checks

    def validate(self, packet: TelemetryPacket) -> ValidationResult:
        """
        Executes the validation chain.

        Returns:
            ValidationResult.ok()         — all checks passed.
            ValidationResult.fail(reason) — first failing check's reason.
        """
        for check in self._checks:
            result = check.check(packet)
            if not result.is_valid:
                return result
        return ValidationResult.ok()
