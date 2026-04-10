from ...domain.models import TelemetryPacket
from ..models import ValidationResult


class ConsistencyCheck:
    """
    IValidationCheck — Step 3 in the Chain of Responsibility.

    Verifies cross-field consistency: relationships that must hold between
    multiple telemetry fields to be physically meaningful.
    """

    def check(self, packet: TelemetryPacket) -> ValidationResult:
        """
        Runs all consistency checks. Returns first failure or ok.
        """
        # If engine is running (rpm > 0), gear must be >= 0.
        # Gear=0 is neutral which is valid, but negative gear is not.
        if packet.CurrentEngineRpm > 0 and packet.Gear < 0:
            return ValidationResult.fail(
                f"Invalid gear {packet.Gear} while engine is running "
                f"(rpm={packet.CurrentEngineRpm:.0f})"
            )

        # MaxRpm must be >= IdleRpm when engine is active
        if packet.EngineMaxRpm > 0 and packet.EngineIdleRpm > packet.EngineMaxRpm:
            return ValidationResult.fail(
                f"EngineIdleRpm ({packet.EngineIdleRpm:.0f}) > "
                f"EngineMaxRpm ({packet.EngineMaxRpm:.0f})"
            )

        # CurrentEngineRpm must not exceed MaxRpm (with 5% tolerance for transients)
        if (
            packet.EngineMaxRpm > 0
            and packet.CurrentEngineRpm > packet.EngineMaxRpm * 1.05
        ):
            return ValidationResult.fail(
                f"CurrentEngineRpm ({packet.CurrentEngineRpm:.0f}) exceeds "
                f"EngineMaxRpm ({packet.EngineMaxRpm:.0f}) by >5%"
            )

        # Drivetrain type must be one of: 0=FWD, 1=RWD, 2=AWD
        if packet.DrivetrainType not in (0, 1, 2):
            return ValidationResult.fail(
                f"Unknown DrivetrainType: {packet.DrivetrainType} (expected 0, 1, or 2)"
            )

        return ValidationResult.ok()
