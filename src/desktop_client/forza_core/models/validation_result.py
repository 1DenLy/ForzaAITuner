import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class ValidationResult:
    """
    Result of IPacketValidator.validate().

    Fields:
        is_valid — True if the TelemetryPacket passed all validation checks.
        reason   — Human-readable reason for rejection. None when is_valid=True.
    """
    is_valid: bool
    reason: str | None = None

    @staticmethod
    def ok() -> "ValidationResult":
        """Factory method for a successful validation result."""
        return ValidationResult(is_valid=True)

    @staticmethod
    def fail(reason: str) -> "ValidationResult":
        """Factory method for a failed validation result."""
        return ValidationResult(is_valid=False, reason=reason)
