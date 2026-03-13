import asyncio
import structlog
import aiohttp
from typing import Any, Callable, List, Optional

from desktop_client.domain.interface.protocols import IBuffer, ISyncWorker
from desktop_client.domain.interface.interfaces import IEventBus
from desktop_client.domain.events import BackendErrorEvent

logger = structlog.get_logger(__name__)


class SyncWorker(ISyncWorker):
    """Sends telemetry batches to the backend REST API.

    Args:
        buffer:      Ring-buffer that holds in-flight telemetry packets.
        api_url:     Full URL of the ingest endpoint.
        serializer:  Pure function that converts a batch of domain objects
                     into a JSON-serialisable ``list[dict]``.  Keeping the
                     conversion logic outside the worker preserves SRP and
                     makes it trivial to swap formats without touching
                     networking code.
        batch_size:  Maximum number of packets per HTTP request.
        interval_sec: How often the send loop fires (seconds).
    """

    def __init__(
        self,
        buffer: IBuffer,
        api_url: str,
        serializer: Callable[[List[Any]], List[dict]],
        batch_size: int = 60,
        interval_sec: float = 1.0,
        event_bus: Optional[IEventBus] = None,
    ) -> None:
        self.buffer = buffer
        self.api_url = api_url
        self._serializer = serializer
        self.batch_size = batch_size
        self.interval_sec = interval_sec
        self._event_bus = event_bus
        self._is_running: bool = False
        self._task: Optional[asyncio.Task] = None
        self._session: Optional[aiohttp.ClientSession] = None

    async def start(self) -> None:
        if self._is_running:
            return
        self._is_running = True
        # Strict lifecycle: session is created here and only here.
        # ClientTimeout covers DNS resolution + TCP handshake + total request.
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5.0)
        )
        self._task = asyncio.create_task(self._run_loop())

    async def _run_loop(self) -> None:
        while self._is_running:
            try:
                await asyncio.sleep(self.interval_sec)

                # Если во время сна вызвали stop(), не забираем новую пачку
                if not self._is_running:
                    break

                with self.buffer.transaction_n(self.batch_size) as batch:
                    if not batch:
                        continue

                    success = await self._send_batch(batch)

                    if not success:
                        logger.warning("Failed to send batch, rolled back.", batch_size=len(batch))
                        raise RuntimeError("send failed")  # triggers automatic rollback

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Unexpected error in SyncWorker run loop.", error=str(e), exc_info=True)

    async def _send_batch(self, batch: List[Any]) -> bool:
        assert self._session is not None, "SyncWorker.start() must be called before sending data"
        try:
            payload = self._serializer(batch)
            async with self._session.post(self.api_url, json=payload) as response:
                if response.status not in (200, 201):
                    logger.warning("Backend error response", status=response.status)
                    if self._event_bus:
                        if response.status == 401:
                            safe_msg = "Authorization failed. Please check your settings."
                        elif response.status >= 500:
                            safe_msg = "Backend server error. Retrying later."
                        else:
                            safe_msg = f"API error occurred (Status: {response.status})."
                        
                        self._event_bus.emit(
                            BackendErrorEvent(
                                code=response.status,
                                message=safe_msg,
                                is_transient=response.status >= 500
                            )
                        )
                    return False
                return True

        except asyncio.TimeoutError:
            logger.warning("Timeout while sending telemetry batch.")
            if self._event_bus:
                self._event_bus.emit(
                    BackendErrorEvent(
                        code=408,
                        message="Connection to server timed out.",
                        is_transient=True
                    )
                )
            return False
        except aiohttp.ClientError as e:
            logger.warning("Network error while sending telemetry batch.", error=str(e))
            if self._event_bus:
                self._event_bus.emit(
                    BackendErrorEvent(
                        code=503,
                        message="Network error. Unable to reach server.",
                        is_transient=True
                    )
                )
            return False
        except Exception as e:
            logger.error("Error serializing or sending batch.", error=str(e), exc_info=True)
            if self._event_bus:
                self._event_bus.emit(
                    BackendErrorEvent(
                        code=500,
                        message="An unexpected client error occurred.",
                        is_transient=False
                    )
                )
            return False

    async def stop(self) -> None:
        self._is_running = False
        if self._task:
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        if self.buffer.size:
            logger.info("Force flush remaining telemetry packets...", count=self.buffer.size)

            # Делаем 3 попытки отправить последние данные
            max_retries = 3
            with self.buffer.transaction() as remaining:
                for attempt in range(max_retries):
                    success = await self._send_batch(remaining)
                    if success:
                        logger.info("Successfully sent remaining telemetry.")
                        break
                    logger.warning("Failed to send remaining telemetry, retrying...", attempt=attempt + 1)
                    if attempt < max_retries - 1:
                        await asyncio.sleep(1.0)
                else:
                    logger.error("Could not send remaining telemetry after retries.")
                    raise RuntimeError("flush failed")  # triggers automatic rollback

        if self._session:
            await self._session.close()
            self._session = None

        logger.info("SyncWorker stopped.")
