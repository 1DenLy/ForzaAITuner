import asyncio
import logging
from datetime import datetime, timezone
from typing import Callable

from .interfaces import ISourceValidator, IRateLimiter
from .models import RawPacket

logger = logging.getLogger(__name__)

# Maximum buffer size for recvfrom().
# Max valid Forza packet = 331 bytes. Buffer = 512 (nearest power of two above 331).
# Oversized datagrams are truncated by the OS at this boundary — before Rate Limiter fires.
_UDP_BUFSIZE = 512


class UdpListener(asyncio.DatagramProtocol):
    """
    Infrastructure Producer: reads raw UDP datagrams from the Forza game.

    Responsibilities (in order per datagram):
      ① Source Validation — delegates to ISourceValidator.is_allowed(ip)
      ② Rate Limiting     — delegates to IRateLimiter.allow(ip)
      ③ Timestamping      — received_at = datetime.now(UTC) immediately after recvfrom()
      ④ Forward           — calls on_packet(RawPacket) callback

    Does NOT:
      - Interpret packet content.
      - Orchestrate the processing pipeline (PipelineManager's job).
      - Write to DLQ — network drops are tracked via metrics only (DoS protection).

    Buffer = 512 bytes (OS truncates oversized datagrams before this class sees them).
    """

    def __init__(
        self,
        source_validator: ISourceValidator,
        rate_limiter: IRateLimiter,
    ) -> None:
        self._source_validator = source_validator
        self._rate_limiter = rate_limiter
        self._transport: asyncio.DatagramTransport | None = None

        # Callback wired by ForzaCore: on_packet = pipeline.enqueue
        self.on_packet: Callable[[RawPacket], None] | None = None

        # Lightweight drop counters (metrics only)
        self._drops_unknown_source: int = 0
        self._drops_rate_limit: int = 0

    # ------------------------------------------------------------------ asyncio

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self._transport = transport  # type: ignore[assignment]
        logger.info("UdpListener: socket bound and listening.")

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        """
        Called by asyncio for each received UDP datagram.

        Steps:
          ① timestamp — before any processing
          ② source validation
          ③ rate limiting
          ④ forward to pipeline via on_packet callback
        """
        # ③ Timestamp is set first — closest to the actual recvfrom() moment.
        received_at = datetime.now(timezone.utc)
        ip = addr[0]

        # ① Source Validation
        if not self._source_validator.is_allowed(ip):
            self._drops_unknown_source += 1
            logger.debug(
                "UdpListener: drop.unknown_source ip=%s total=%d",
                ip, self._drops_unknown_source,
            )
            return

        # ② Rate Limiting
        if not self._rate_limiter.allow(ip):
            self._drops_rate_limit += 1
            logger.debug(
                "UdpListener: drop.rate_limit ip=%s total=%d",
                ip, self._drops_rate_limit,
            )
            return

        # ④ Forward
        packet = RawPacket(data=data, source_ip=ip, received_at=received_at)
        if self.on_packet:
            self.on_packet(packet)

    def error_received(self, exc: Exception) -> None:
        logger.error("UdpListener: socket error: %s", exc)

    def connection_lost(self, exc: Exception | None) -> None:
        if exc:
            logger.error("UdpListener: connection lost: %s", exc)
        else:
            logger.info("UdpListener: socket closed.")

    # ------------------------------------------------------------------ lifecycle

    async def start(self, host: str, port: int) -> None:
        """
        Opens the UDP socket and begins receiving datagrams asynchronously.
        Called by ForzaCore via IAsyncRunner.submit().
        """
        loop = asyncio.get_running_loop()
        await loop.create_datagram_endpoint(
            lambda: self,
            local_addr=(host, port),
        )
        logger.info("UdpListener: listening on %s:%d (bufsize=%d)", host, port, _UDP_BUFSIZE)

    def stop(self) -> None:
        """
        Closes the UDP socket. Remaining datagrams in the OS buffer are discarded.
        Called by ForzaCore during stop_tracking().
        """
        if self._transport is not None:
            self._transport.close()
            self._transport = None
            logger.info("UdpListener: stopped.")
