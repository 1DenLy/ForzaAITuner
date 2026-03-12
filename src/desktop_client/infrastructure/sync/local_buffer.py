import threading
from collections import deque
from contextlib import contextmanager
from typing import Any, Generator, List


class LocalBuffer:
    def __init__(self, maxsize: int = 60000):
        self._maxsize = maxsize
        self._queue = deque(maxlen=maxsize)
        self._pending_batch: List[Any] = []
        self._lock = threading.Lock()

    def put_nowait(self, packet: Any) -> bool:
        """Enqueue a packet. If the buffer is at capacity, the oldest element is removed."""
        with self._lock:
            self._queue.append(packet)
            return True

    def take_batch(self, n: int) -> List[Any]:
        with self._lock:
            if self._pending_batch:
                return list(self._pending_batch)  # shallow copy — caller cannot mutate internal state

            batch = []
            for _ in range(min(n, len(self._queue))):
                batch.append(self._queue.popleft())

            self._pending_batch = batch
            return list(self._pending_batch)  # shallow copy

    def take_all_remaining(self) -> List[Any]:
        with self._lock:
            self._pending_batch.extend(self._queue)
            self._queue.clear()
            return list(self._pending_batch)  # shallow copy — caller cannot mutate internal state

    @contextmanager
    def transaction(self) -> Generator[List[Any], None, None]:
        """Context manager that auto-commits on success and rolls back on any exit.

        Grabs **all** items currently in the buffer (including any pending batch).
        Uses ``finally`` so that ``BaseException`` subclasses (``CancelledError``,
        ``KeyboardInterrupt``, ``SystemExit``) also trigger a rollback.

        Usage::

            with buffer.transaction() as batch:
                send(batch)
                # commit runs automatically on clean exit
                # rollback runs automatically on any exception/cancellation
        """
        batch = self.take_all_remaining()
        committed = False
        try:
            yield batch
            self._commit()
            committed = True
        finally:
            if not committed:
                self._rollback()

    @contextmanager
    def transaction_n(self, n: int) -> Generator[List[Any], None, None]:
        """Like ``transaction()``, but takes at most *n* items from the queue.

        Usage::

            with buffer.transaction_n(batch_size) as batch:
                send(batch)
        """
        batch = self.take_batch(n)
        committed = False
        try:
            yield batch
            self._commit()
            committed = True
        finally:
            if not committed:
                self._rollback()

    # ------------------------------------------------------------------
    # Internal helpers — not part of the public API
    # ------------------------------------------------------------------

    def _commit(self) -> None:
        with self._lock:
            self._pending_batch.clear()

    def _rollback(self) -> None:
        with self._lock:
            self._queue.extendleft(reversed(self._pending_batch))
            self._pending_batch.clear()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._queue) + len(self._pending_batch)
