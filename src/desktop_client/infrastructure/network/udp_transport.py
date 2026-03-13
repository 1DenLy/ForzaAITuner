import asyncio
import logging
import time
from typing import Optional, Tuple

try:
    from typing import override
except ImportError:
    from typing_extensions import override

from desktop_client.validation import PacketValidator

logger = logging.getLogger(__name__)

class UdpListener(asyncio.DatagramProtocol):
    """
    High-performance UDP listener for Forza Telemetry.
    Implements 'Fail Fast' rule: drops invalid packets immediately.
    """
    def __init__(self, queue: asyncio.Queue, validator: PacketValidator):
        self.queue = queue
        self._validator = validator
        self._last_error_log_time = 0.0
        self.dropped_packets = 0

    @override
    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        logger.info("udp_transport_connected")

    @override
    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        """
        Receive datagram, validate size immediately, and push to queue.
        """
        # 1. Fail Fast Validation
        result = self._validator.validate(data)
        if not result.is_valid:
            self.dropped_packets += 1
            now = time.time()
            if now - self._last_error_log_time >= 1.0:
                logger.warning(
                    "udp_packet_dropped", 
                    reason=result.errors[0].message, 
                    size=len(data),
                    total_dropped=self.dropped_packets
                )
                self._last_error_log_time = now
            return

        # 2. Push to queue (Drop Tail if full)
        try:
            self.queue.put_nowait((data, addr))
        except asyncio.QueueFull:
            self.dropped_packets += 1
            now = time.time()
            if now - self._last_error_log_time >= 1.0:
                logger.warning("udp_queue_full_dropped_packet")
                self._last_error_log_time = now

    @override
    def error_received(self, exc: Exception) -> None:
        logger.error(f"udp_transport_error: {exc}")
