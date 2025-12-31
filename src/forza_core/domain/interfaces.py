from typing import Protocol, List
from .models import TelemetryPacket

class ITelemetryRepository(Protocol):
    """
    Interface for storing telemetry packets.
    Write-Only (ISP).
    """
    async def save_batch(self, packets: List[TelemetryPacket]) -> None:
        """
        Asynchronously save a batch of telemetry packets.
        """
        ...
