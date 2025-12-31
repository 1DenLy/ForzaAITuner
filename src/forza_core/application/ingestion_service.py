import asyncio
import structlog
import dataclasses
from typing import List, Optional
from ..domain.models import TelemetryPacket
from ..domain.interfaces import ITelemetryRepository
from ..domain.events import RaceStarted
from ..config import IngestionConfig
from .packet_parser import PacketParser

logger = structlog.get_logger()

class IngestionService:
    """
    Orchestrates telemetry ingestion, parsing, buffering, and storage.
    """
    def __init__(
        self, 
        repo: ITelemetryRepository, 
        config: IngestionConfig, 
        queue: asyncio.Queue
    ):
        self._repo = repo
        self._config = config
        self._queue = queue
        self._buffer: List[TelemetryPacket] = []
        self._last_is_race_on = 0
        self._running = False

    async def run(self) -> None:
        """
        Main run loop: consuming from queue, parsing, buffering.
        """
        self._running = True
        logger.info("ingestion_service_started")
        
        while self._running:
            try:
                # Get raw packet from queue
                data, addr = await self._queue.get()
                
                try:
                    packet = PacketParser.parse(data)
                except ValueError as e:
                    logger.warning("packet_parse_error", error=str(e))
                    self._queue.task_done()
                    continue
                
                await self._process_packet(packet)
                self._queue.task_done()
                
            except asyncio.CancelledError:
                logger.info("ingestion_service_cancelled")
                self._running = False
                break
            except Exception as e:
                logger.error("ingestion_service_error", error=str(e), exc_info=True)
                # Continue loop to avoid crash
                await asyncio.sleep(0.1)

    async def _process_packet(self, packet: TelemetryPacket) -> None:
        """
        State machine and buffering logic.
        """
        # State Machine: IsRaceOn 0 -> 1 (Race Started)
        if self._last_is_race_on == 0 and packet.is_race_on == 1:
            event = RaceStarted(
                timestamp=packet.current_race_time,
                car_ordinal=packet.car_ordinal,
                car_class=packet.car_class,
                car_performance_index=packet.car_performance_index
            )
            logger.info("race_started", event=dataclasses.asdict(event)) # dataclasses is not imported, need to import it or use other way.
            # actually better to just log fields or fix import.

        # State Machine: IsRaceOn 1 -> 0 (Race Ended)
        if self._last_is_race_on == 1 and packet.is_race_on == 0:
            logger.info("race_ended")
            # Flush existing buffer
            await self._flush()
            self._buffer.clear()

        self._last_is_race_on = packet.is_race_on
        
        # Buffer Logic
        if packet.is_race_on == 1:
            self._buffer.append(packet)
            
            if len(self._buffer) >= self._config.BUFFER_SIZE:
                await self._flush()

    async def _flush(self) -> None:
        """
        Flush buffer to repository.
        """
        if not self._buffer:
            return

        try:
            await self._repo.save_batch(list(self._buffer)) # Create copy to be safe
            self._buffer.clear()
        except Exception as e:
            logger.error("flush_error", error=str(e))
            # Decision: drop buffer or keep?
            # Spec says "Сбросить буфер" implies we consume it even on error to avoid memory leak?
            # Or "Обернут в try/except для логирования ошибок БД, чтобы сервис не упал."
            # Usually we might want to retry, but for "Zero-latency" and preventing overflow, dropping might be safer or keeping for next retry.
            # But the requirement says "Очищает буфер" inside _flush method logic description.
            # Wait, spec says:
            # Метод _flush:
            # Отправляет данные в репозиторий.
            # Очищает буфер.
            # Обернут в try/except...
            
            # Implementation above clears it only if successful? 
            # I should clearer logic: try send -> except log -> finally clear is typical for lossy telemetry.
            # But for "Data Collection" we might want retention.
            # Given High Throughput nature, blocking/infinite retry is bad.
            # I will clear buffer to prevent OOM locally.
            self._buffer.clear()

    async def flush(self) -> None:
        """Public flush for watchdog/shutdown."""
        await self._flush()


