import threading
from collections import deque
from typing import Any, List


class LocalBuffer:
    def __init__(self, maxsize: int = 60000):
        self._maxsize = maxsize
        self._queue = deque(maxlen=maxsize)
        self._pending_batch = []
        self._lock = threading.Lock()

    def put_nowait(self, packet: Any) -> None:
        with self._lock:
            self._queue.append(packet)

    def take_batch(self, n: int) -> List[Any]:
        with self._lock:
            if self._pending_batch:
                return self._pending_batch
            
            batch = []
            for _ in range(min(n, len(self._queue))):
                batch.append(self._queue.popleft())
                
            self._pending_batch = batch
            return self._pending_batch

    def commit(self) -> None:
        with self._lock:
            self._pending_batch.clear()

    def rollback(self) -> None:
        with self._lock:
            self._queue.extendleft(reversed(self._pending_batch))
            self._pending_batch.clear()

    def take_ALL_remaining(self) -> List[Any]:
        with self._lock:
            self._pending_batch.extend(self._queue)
            self._queue.clear()
            return self._pending_batch

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._queue) + len(self._pending_batch)
