from typing import Protocol
from ..models import RawPacket


class IPipelineManager(Protocol):
    """
    Application interface for the pipeline Consumer component.

    Responsibilities:
    - Accept RawPacket via enqueue() into an internal InQueue.
    - Orchestrate the Decode → Parse → Validate chain in Worker thread(s).
    - Route errors to DLQ and metrics.
    - Push valid TelemetryPacket items to OutQueue.

    Does NOT know about the network. Does NOT manage module lifecycle (ForzaCore's job).
    """

    def start(self) -> None:
        """Initialises InQueue and starts the Worker pool."""
        ...

    def stop(self) -> None:
        """Drains the remaining queue items and shuts down workers gracefully."""
        ...

    def enqueue(self, packet: RawPacket) -> None:
        """
        Called by UdpListener (via on_packet callback).
        Places the RawPacket into the InQueue for asynchronous processing.
        """
        ...
