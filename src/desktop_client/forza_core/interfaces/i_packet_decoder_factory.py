from typing import Protocol
from .i_packet_decoder import IPacketDecoder


class IPacketDecoderFactory(Protocol):
    """
    Registry-based factory for selecting the correct IPacketDecoder by packet size.

    Uses a Map<int, IPacketDecoder> registry instead of if/switch chains.
    Adding a new decoder = one register() call. Zero modifications to existing code (OCP).
    """

    def get_decoder(self, size: int) -> IPacketDecoder | None:
        """
        Returns the registered IPacketDecoder for the given packet size.

        Returns:
            IPacketDecoder — if a decoder is registered for this size.
            None           — if size is unknown (PipelineManager will drop with metrics only).
        """
        ...
