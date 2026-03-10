from typing import Protocol, List, Any

class IBuffer(Protocol):
    """
    Consumer-agnostic interface for reading telemetry data asynchronously.
    """
    async def async_wait_for_data(self) -> None:
        """Wait until there is at least one packet in the buffer."""
        ...
        
    def get_all_nowait(self) -> List[Any]:
        """Retrieve and remove all currently available packets without blocking."""
        ...


class ISyncWorker(Protocol):
    """
    Interface for the background service that synchronizes local data with a remote API.
    """
    async def start(self) -> None:
        """Start the background synchronization loop."""
        ...

    async def stop(self) -> None:
        """Stop the loop and perform a final flush of remaining data."""
        ...
