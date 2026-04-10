from ..interfaces import IPacketDecoder


class PacketDecoderFactory:
    """
    Registry-based factory for IPacketDecoder selection.

    Uses a dict[int, IPacketDecoder] registry instead of if/switch chains.
    Adding a new decoder = one register() call at the Composition Root.
    Zero modifications to existing decoder code (Open/Closed Principle).

    Usage (Composition Root / main.py):
        factory = PacketDecoderFactory()
        factory.register(311, Fm7Decoder())
        factory.register(324, Fh4Decoder())
        factory.register(331, Fh5Decoder())
    """

    def __init__(self) -> None:
        self._registry: dict[int, IPacketDecoder] = {}

    def register(self, size: int, decoder: IPacketDecoder) -> None:
        """
        Registers a decoder for a specific packet size.

        Args:
            size    — exact byte count of the packet this decoder handles.
            decoder — IPacketDecoder instance to return for this size.
        """
        self._registry[size] = decoder

    def get_decoder(self, size: int) -> IPacketDecoder | None:
        """
        Returns the registered decoder for the given packet size.

        Returns:
            IPacketDecoder — if registered.
            None           — if unknown size (PipelineManager drops with metrics only).
        """
        return self._registry.get(size)
