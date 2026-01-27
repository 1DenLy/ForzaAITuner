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

    async def create_session(self, car_ordinal: int, track_id: str, tuning_config_id: int | None = None) -> int:
        """
        Create a new session record and return its ID.
        """
        ...


class IPacketParser(Protocol):
    """
    Interface for parsing raw bytes into a TelemetryPacket.
    """
    def parse(self, data: bytes) -> TelemetryPacket | None:
        """
        Parses binary data. Returns None if data is invalid/unsupported.
        """
        ...
