import asyncio
import structlog
import dataclasses
import time
from typing import List, Optional, Set
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
        self._flush_lock = asyncio.Lock()
        self._last_flush_time = 0.0
        self._active_saves: Set[asyncio.Task] = set()

    async def run(self) -> None:
        """
        Main run loop: consuming from queue, parsing, buffering.
        Consumption is decoupled from Flushing via background tasks.
        """
        self._running = True
        logger.info("ingestion_service_started")
        
        # Start background flush monitor
        monitor_task = asyncio.create_task(self._monitor_flush())
        
        try:
            while self._running:
                try:
                    # Pure consumer loop, no blocking on IO
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
                    raise
                except Exception as e:
                    logger.error("ingestion_service_error", error=str(e), exc_info=True)
                    await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            logger.info("ingestion_service_cancelled")
        finally:
            self._running = False
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

    async def _monitor_flush(self) -> None:
        """Background task to trigger time-based flushes."""
        logger.info("flush_monitor_started")
        while self._running:
            try:
                await asyncio.sleep(0.1) # Check every 100ms
                if not self._buffer:
                    continue
                    
                time_since = time.time() - self._last_flush_time
                if time_since >= self._config.flush_interval_sec:
                    await self._flush()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("flush_monitor_error", error=str(e))

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
            logger.info("race_started", race_data=dataclasses.asdict(event)) 

        # State Machine: IsRaceOn 1 -> 0 (Race Ended)
        if self._last_is_race_on == 1 and packet.is_race_on == 0:
            logger.info("race_ended")
            # Force flush on race end
            await self._flush()

        self._last_is_race_on = packet.is_race_on
        
        # Buffer Logic
        if packet.is_race_on == 1:
            self._buffer.append(packet)
            
            if len(self._buffer) >= self._config.buffer_size:
                await self._flush()

    async def _flush(self) -> None:
        """
        Prepares buffer for flushing and spawns a background save task.
        Non-blocking for the consumer loop.
        """
        async with self._flush_lock:
            if not self._buffer:
                return
            
            # Swap buffer (Double Buffering)
            packets_to_save = list(self._buffer)
            self._buffer.clear()
            self._last_flush_time = time.time()
            
        # Spawn fire-and-forget save task
        task = asyncio.create_task(self._save_safe(packets_to_save))
        
        # Track active saves
        self._active_saves.add(task)
        task.add_done_callback(self._active_saves.discard)

    async def _save_safe(self, packets: List[TelemetryPacket]) -> None:
        """
        Execute DB save with error handling.
        """
        try:
            await self._repo.save_batch(packets)
        except Exception as e:
            dropped_count = len(packets)
            logger.error("flush_error", error=str(e), dropped_count=dropped_count)

    async def flush(self) -> None:
        """
        Public flush for watchdog/shutdown.
        Waits for ALL pending saves to complete.
        """
        # 1. Trigger final swap
        await self._flush()
        
        # 2. Wait for all background tasks to finish
        if self._active_saves:
            logger.info("waiting_for_pending_saves", count=len(self._active_saves))
            await asyncio.gather(*self._active_saves, return_exceptions=True)
