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
    def put_nowait(self, item: TelemetryPacket) -> None:
        """
        Puts an item into the queue without blocking.
        Expected to raise asyncio.QueueFull if the queue is full,
        or handle it internally.
        """
        ...
