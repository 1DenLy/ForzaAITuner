import asyncio
import logging
import time
from typing import Optional, Tuple

try:
    from typing import Override # Python 3.12+
except ImportError:
    from typing_extensions import Override

logger = logging.getLogger(__name__) # Use standard logger which is hooked

class UdpListener(asyncio.DatagramProtocol):
    """
    High-performance UDP listener for Forza Telemetry.
    """
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self._last_error_log_time = 0.0

    @Override
    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        logger.info("udp_transport_connected")

    @Override
    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        """
        Receive datagram and push to queue. Zero-latency.
        Implements Drop Tail strategy via put_nowait.
        """
        try:
            self.queue.put_nowait((data, addr))
        except asyncio.QueueFull:
            # Drop Tail strategy: Just ignore new packets if queue is full.
            # Log with rate limiting to avoid spamming I/O.
            now = time.time()
            if now - self._last_error_log_time >= 1.0:
                logger.warning("udp_queue_full_dropped_packet")
                self._last_error_log_time = now
        except Exception as e:
            # Throttling logs: max 1 per second
            now = time.time()
            if now - self._last_error_log_time >= 1.0:
                logger.warning(f"udp_receive_error: {e}")
                self._last_error_log_time = now

    @Override
    def error_received(self, exc: Exception) -> None:
        logger.error(f"udp_transport_error: {exc}")
