from ...domain.models import TelemetryPacket
from ..models import ValidationResult


class RangeCheck:
    """
    IValidationCheck — Step 2 in the Chain of Responsibility.

    Verifies that key telemetry fields fall within physically plausible ranges.
    Rejects packets with values that are structurally valid (not NaN) but
    physically impossible (e.g. rpm > 20000, speed > 500 km/h).
    """

    # Speed is stored in m/s in TelemetryPacket. 500 km/h ≈ 138.9 m/s
    _MAX_SPEED_MPS: float = 140.0
    _MAX_RPM: float = 20_000.0
    _MAX_BOOST: float = 3.0       # bar, typical turbo range
    _MAX_FUEL: float = 1.0        # normalised [0..1]
    _MIN_PI: int = 100
    _MAX_PI: int = 999

    def check(self, packet: TelemetryPacket) -> ValidationResult:
        """
        Runs all range checks. Returns the first failure or ok.
        """
        if not (0.0 <= packet.Speed <= self._MAX_SPEED_MPS):
            return ValidationResult.fail(
                f"Speed out of range: {packet.Speed:.2f} m/s (max {self._MAX_SPEED_MPS})"
            )

        if not (0.0 <= packet.CurrentEngineRpm <= self._MAX_RPM):
            return ValidationResult.fail(
                f"CurrentEngineRpm out of range: {packet.CurrentEngineRpm:.0f} "
                f"(0..{self._MAX_RPM:.0f})"
            )

        if not (0.0 <= packet.EngineMaxRpm <= self._MAX_RPM):
            return ValidationResult.fail(
                f"EngineMaxRpm out of range: {packet.EngineMaxRpm:.0f}"
            )

        if not (0.0 <= packet.Fuel <= self._MAX_FUEL):
            return ValidationResult.fail(
                f"Fuel out of range: {packet.Fuel:.3f} (expected 0..1)"
            )

        if packet.CarPerformanceIndex != 0 and not (
            self._MIN_PI <= packet.CarPerformanceIndex <= self._MAX_PI
        ):
            return ValidationResult.fail(
                f"CarPerformanceIndex out of range: {packet.CarPerformanceIndex} "
                f"({self._MIN_PI}..{self._MAX_PI})"
            )

        if not (0 <= packet.Gear <= 15):
            return ValidationResult.fail(
                f"Gear out of range: {packet.Gear} (0..15)"
            )

        return ValidationResult.ok()
