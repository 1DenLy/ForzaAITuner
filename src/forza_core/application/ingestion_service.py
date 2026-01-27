import asyncio
import structlog
import dataclasses
import time
from typing import List, Optional, Set
from ..domain.models import TelemetryPacket
from ..domain.interfaces import ITelemetryRepository
from ..domain.events import RaceStarted
from ..config import IngestionConfig
from .race_monitor import RaceStateMonitor
from ..domain.interfaces import IPacketParser

class IngestionService:
    """
    Orchestrates telemetry ingestion, parsing, buffering, and storage.
    """
    def __init__(
        self, 
        repo: ITelemetryRepository, 
        config: IngestionConfig, 
        queue: asyncio.Queue,
        parser: IPacketParser
    ):
        self._repo = repo
        self._config = config
        self._queue = queue
        self._parser = parser
        self._buffer: List[TelemetryPacket] = []
        self._monitor = RaceStateMonitor()
        self._running = False
        self._flush_lock = asyncio.Lock()
        self._last_flush_time = 0.0
        self._active_saves: Set[asyncio.Task] = set()
        
        # Session Context
        self._current_session_id: Optional[int] = None
        self._session_lock = asyncio.Lock()

    # ... set_session and stop_session remain unchanged ...

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
                    
                    # 1. Parse via injected Interface
                    packet = self._parser.parse(data)
                    
                    # 2. Handle invalid packets (None)
                    if not packet:
                        # Log warning? Already logged in parser if we want logic there?
                        # Or generic log here.
                        # logger.warning("invalid_packet_dropped", len=len(data)) 
                        # Parser returns None on error, we assume it handles internal low-level logging or we do.
                        # Let's skip without log spam.
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

    async def _process_packet(self, packet: TelemetryPacket) -> None:
        """
        State machine and buffering logic.
        """
        # 3. Detect Events via Monitor
        events = self._monitor.detect_events(packet)
        for event in events:
             if isinstance(event, RaceStarted):
                 logger.info("race_started", race_data=dataclasses.asdict(event)) 
             # Handle other events if any

        # Buffer Logic
        if packet.is_race_on == 1:
            # 4. Immutable Fix: Create new instance with session_id
            # Note: We must read session context under lock if we want strict consistency, 
            # or accept slight race (eventual consistency).
            # given it's a high freq loop, we might read the atomic reference (single Python op).
            # self._current_session_id reading is atomic in GIL.
            
            enrichment = {}
            if self._current_session_id:
                enrichment['session_id'] = self._current_session_id
            
            # Create COPY with changes
            enriched_packet = dataclasses.replace(packet, **enrichment)

            self._buffer.append(enriched_packet)
            
            if len(self._buffer) >= self._config.buffer_size:
                await self._flush()
        else:
            # If race stopped, check if we need to flush last batch?
            # The monitor tracks state.
            pass

    async def set_session(self, car_ordinal: int, track_id: str, tuning_config_id: Optional[int] = None) -> None:
        """Sets the current session context by creating a record in DB."""
        async with self._session_lock:
             try:
                 new_id = await self._repo.create_session(car_ordinal, track_id, tuning_config_id)
                 self._current_session_id = new_id
                 logger.info("session_context_set", session_id=self._current_session_id, car=car_ordinal)
             except Exception as e:
                 logger.error("session_creation_failed", error=str(e))
                 # Fallback/Fail logic? For now just log.

    async def stop_session(self) -> None:
        """Clears the current session context."""
        async with self._session_lock:
            last_id = self._current_session_id
            self._current_session_id = None
            logger.info("session_context_cleared", last_session_id=last_id)


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
        Execute DB save with retry logic (Reliability).
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self._repo.save_batch(packets)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning("flush_retry", attempt=attempt+1, error=str(e))
                    await asyncio.sleep(0.5 * (attempt + 1)) # Simple backoff
                else:
                    dropped_count = len(packets)
                    logger.error("flush_error_final", error=str(e), dropped_count=dropped_count)

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
