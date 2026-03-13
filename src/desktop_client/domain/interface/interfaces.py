from typing import Protocol, Any
from ..models import TelemetryPacket

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

class IAsyncRunner(Protocol):
    """
    Interface for running an asyncio event loop in a dedicated environment (e.g., background thread).
    """
    def start(self) -> None:
        """Starts the runner environment."""
        ...

    def stop(self) -> None:
        """Stops the runner environment gracefully."""
        ...

    def submit(self, coro: 'asyncio.coroutine') -> 'asyncio.Future': # type: ignore
        """Submits a coroutine to run in the managed event loop from another thread."""
        ...


class ICoreFacade(Protocol):
    """
    Interface for interacting with the Core Application logic.
    Decouples Presentation Layer from specific Core implementations.
    """
    def start_tracking(self) -> None:
        """Starts the race session tracking/recording."""
        ...

    def stop_tracking(self) -> None:
        """Stops the race session tracking."""
        ...

    def cleanup(self) -> None:
        """Performs cleanup operations (e.g. closing connections) for graceful shutdown."""
        ...

    def is_tracking(self) -> bool:
        """Returns True if a session is currently being tracked."""
        ...


class ITelemetryManager(Protocol):
    """
    Interface for the telemetry session manager.
    Coordinates telemetry pipeline start/stop.
    """
    async def start_session(self) -> None:
        ...

    async def stop_session(self) -> None:
        ...


class IEventBus(Protocol):
    """
    Interface for cross-module event dispatching.
    Decouples infrastructure (like PySide6 Signals) from application logic.
    """
    def emit(self, event: Any) -> None:
        """
        Dispatches an event to all interested subscribers.
        """
        ...
