from typing import Protocol, Callable
from ..models import RawPacket


class IUdpListener(Protocol):
    """
    Infrastructure interface for the UDP Producer component.

    Responsibilities:
    - Read raw bytes from a UDP socket (recvfrom).
    - Delegate Source Validation to ISourceValidator.
    - Delegate Rate Limiting to IRateLimiter.
    - Attach received_at timestamp immediately after recvfrom().
    - Fire on_packet callback with the resulting RawPacket.

    Does NOT interpret packet content, does NOT orchestrate the pipeline.
    """

    on_packet: Callable[[RawPacket], None]
    """
    Callback set by ForzaCore to route packets into the pipeline.
    Must be assigned before calling start().
    """

    def start(self, host: str, port: int) -> None:
        """Binds the UDP socket and starts listening asynchronously."""
        ...

    def stop(self) -> None:
        """Stops listening and releases the socket."""
        ...
