import dataclasses
from datetime import datetime


@dataclasses.dataclass(frozen=True, slots=True)
class RawPacket:
    """
    Represents a raw UDP datagram received from the Forza game.

    Produced by: UdpListener (after Source Validation, Rate Limiting, and Timestamping).
    Consumed by: PipelineManager (enqueued into InQueue).

    Fields:
        data        — raw bytes as received from recvfrom().
        source_ip   — sender IP address (used for Source Validation and Rate Limiting upstream).
        received_at — UTC timestamp set immediately after recvfrom(), before any processing.
    """
    data: bytes
    source_ip: str
    received_at: datetime
