from typing import Protocol
from ..models import RawTelemetry
from ...domain.models import TelemetryPacket


class IPacketParser(Protocol):
    """
    Domain interface for mapping decoded primitives to the domain model.

    Parse = RawTelemetry (primitives) → TelemetryPacket (domain model).
    This is pure field mapping with unit conversion. NO validation.

    If RawTelemetry contains NaN or anomalous values, the parser maps them
    faithfully. Validation is the responsibility of IPacketValidator.
    """

    def parse(self, raw: RawTelemetry) -> TelemetryPacket:
        """
        Maps RawTelemetry fields to TelemetryPacket domain model.

        Raises:
            struct.error or TypeError — only on physical mapping impossibility
            (e.g. type mismatch). PipelineManager routes these to DLQ as PARSE_ERROR.
        Does NOT drop packets. All accept/reject decisions belong to IPacketValidator.
        """
        ...
