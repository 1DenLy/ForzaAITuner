import asyncio
import logging
import threading
from typing import Coroutine, Any, TypeVar

from desktop_client.forza_core.domain.interfaces import IAsyncRunner

logger = logging.getLogger(__name__)

T = TypeVar('T')

class AsyncioThreadRunner(IAsyncRunner):
    """
    Manages a dedicated asyncio Event Loop running in a background OS thread.
    This resolves SRP violation by moving infrastructure lifecycle out of the application facade.
    """
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)

    def start(self) -> None:
        """Starts the background thread and the event loop."""
        if not self._loop_thread.is_alive():
            self._loop_thread.start()

    def _run_event_loop(self) -> None:
        """Runs the asyncio event loop in a dedicated background thread."""
        logger.info("AsyncioThreadRunner: event loop thread started.")
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
        finally:
            self._loop.close()
            logger.info("AsyncioThreadRunner: event loop thread stopped.")

    def submit(self, coro: Coroutine[Any, Any, T]) -> asyncio.Future[T]:
        """Schedules a coroutine from another thread and returns a concurrent.futures.Future."""
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    def stop(self) -> None:
        """Safely stops the event loop, cancelling all pending tasks."""
        logger.info("AsyncioThreadRunner: stopping event loop...")
        if self._loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self._cancel_and_wait_tasks(), self._loop)
            try:
                future.result(timeout=3.0)
            except Exception as e:
                logger.error(f"Error while waiting for tasks to cancel: {e}")
            self._loop.call_soon_threadsafe(self._loop.stop)
            
        if self._loop_thread.is_alive():
            self._loop_thread.join(timeout=2.0)

    async def _cancel_and_wait_tasks(self) -> None:
        """Cancels all active tasks in the current event loop and waits for them."""
        current_task = asyncio.current_task(self._loop)
        tasks = [t for t in asyncio.all_tasks(self._loop) if t is not current_task]

        for task in tasks:
            task.cancel()

        if tasks:
            # wait for all tasks to finish cancellation, catching CancelledError safely via return_exceptions
            await asyncio.gather(*tasks, return_exceptions=True)
