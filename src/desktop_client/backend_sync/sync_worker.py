import asyncio
import structlog
import aiohttp
from dataclasses import asdict, is_dataclass
from typing import Any, List, Optional

from desktop_client.backend_sync.local_buffer import LocalBuffer

logger = structlog.get_logger(__name__)

class SyncWorker:
    def __init__(self, buffer: LocalBuffer, api_url: str, batch_size: int = 60, interval_sec: float = 1.0):
        self.buffer = buffer
        self.api_url = api_url
        self.batch_size = batch_size
        self.interval_sec = interval_sec
        self._is_running: bool = False
        self._task: Optional[asyncio.Task] = None
        self._session: Optional[aiohttp.ClientSession] = None

    async def start(self) -> None:
        self._is_running = True
        self._session = aiohttp.ClientSession()
        self._task = asyncio.create_task(self._run_loop())

    async def _run_loop(self) -> None:
        while self._is_running:
            try:
                await asyncio.sleep(self.interval_sec)
                
                # Если во время сна вызвали stop(), не забираем новую пачку
                if not self._is_running:
                    break

                batch = self.buffer.take_batch(self.batch_size)
                if not batch:
                    continue
                
                success = await self._send_batch(batch)
                
                if success:
                    self.buffer.commit()
                else:
                    self.buffer.rollback()
                    logger.warning("Failed to send batch, rolled back.", batch_size=len(batch))
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Unexpected error in SyncWorker run loop.", error=str(e), exc_info=True)

    async def _send_batch(self, batch: List[Any]) -> bool:
        try:
            # Сериализация пачки объектов
            payload = [asdict(item) if is_dataclass(item) else item for item in batch]
            
            if self._session is None:
                self._session = aiohttp.ClientSession()
                
            async with self._session.post(self.api_url, json=payload, timeout=5.0) as response:
                return response.status in (200, 201)
                    
        except asyncio.TimeoutError:
            logger.warning("Timeout while sending telemetry batch.")
            return False
        except aiohttp.ClientError as e:
            logger.warning("Network error while sending telemetry batch.", error=str(e))
            return False
        except Exception as e:
            logger.error("Error serializing or sending batch.", error=str(e), exc_info=True)
            return False

    async def stop(self) -> None:
        self._is_running = False
        if self._task:
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            
        remaining = self.buffer.take_ALL_remaining()
        if remaining:
            logger.info("Force flush remaining telemetry packets...", count=len(remaining))
            
            # Делаем 3 попытки отправить последние данные
            max_retries = 3
            for attempt in range(max_retries):
                success = await self._send_batch(remaining)
                if success:
                    self.buffer.commit()
                    logger.info("Successfully sent remaining telemetry.")
                    break
                else:
                    logger.warning("Failed to send remaining telemetry, retrying...", attempt=attempt+1)
                    if attempt < max_retries - 1:
                        await asyncio.sleep(1.0)
            else:
                logger.error("Could not send remaining telemetry after retries.")
                
        if self._session:
            await self._session.close()
            
        logger.info("SyncWorker stopped.")
