from typing import Protocol
from .models import TelemetryPacket

class IPacketParser(Protocol):
    """
    Interface for parsing raw bytes into a TelemetryPacket.
    """
    def parse(self, data: bytes) -> TelemetryPacket | None:
        """
        Parses binary data. Returns None if data is invalid/unsupported.
        """
        ...

class IOutQueue(Protocol):
    """
    Interface for an outbound queue that receives telemetry packets.
    """
    def put_nowait(self, item: TelemetryPacket) -> bool:
        """
        Puts an item into the queue without blocking.

        Returns:
            True  — item was successfully enqueued.
            False — queue is full; item was dropped.

        The caller must NOT catch any infrastructure-specific exceptions
        (e.g. asyncio.QueueFull). All capacity semantics are encapsulated
        inside the concrete adapter.
        """
        ...
