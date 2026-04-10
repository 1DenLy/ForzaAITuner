from datetime import datetime
from typing import Protocol
from ..models import RawTelemetry


class IPacketDecoder(Protocol):
    """
    Interface for binary decoding of a Forza telemetry packet.

    Decode = bytes → RawTelemetry (set of primitives via struct.unpack).
    This is NOT parsing and NOT domain mapping.

    The version of Forza is determined externally by IPacketDecoderFactory,
    not inside the decoder itself.
    """

    def decode(self, data: bytes, received_at: datetime) -> RawTelemetry:
        """
        Unpacks the binary payload into a RawTelemetry of typed primitives.

        Args:
            data: Binary payload from the network.
            received_at: Network-level timestamp of when the packet was received.

        Raises:
            struct.error — if the data is corrupted or has unexpected layout.
        Does NOT return None; error routing is the caller's (PipelineManager) responsibility.
        """
        ...
