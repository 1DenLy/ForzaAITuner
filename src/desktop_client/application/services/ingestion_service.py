import asyncio
import structlog
import dataclasses
from ...domain.models import TelemetryPacket
from ...domain.events import RaceStarted, RaceStopped
from .race_monitor import RaceStateMonitor
from ...domain.interface.interfaces import IPacketParser, IOutQueue
from ...validation import TelemetrySanityValidator
import time

logger = structlog.get_logger()

class IngestionService:
    """
    Orchestrates telemetry ingestion, parsing, and routing.
    """
    def __init__(
        self, 
        queue: asyncio.Queue,
        out_queue: IOutQueue,
        parser: IPacketParser,
        sanity_validator: TelemetrySanityValidator
    ):
        self._queue = queue
        self._out_queue = out_queue
        self._parser = parser
        self._sanity_validator = sanity_validator
        self._monitor = RaceStateMonitor()
        self._running = False
        self._last_sanity_error_time = 0.0

    async def run(self) -> None:
        """
        Main run loop: consuming from queue, parsing, routing to out_queue.
        """
        self._running = True
        logger.info("ingestion_service_started")
        
        try:
            while self._running:
                try:
                    data, addr = await self._queue.get()
                except asyncio.CancelledError:
                    raise

                try:
                    packet = self._parser.parse(data)
                    if packet:
                        # Sanity Check (NaN/Inf)
                        res = self._sanity_validator.validate(packet)
                        if not res.is_valid:
                            now = time.time()
                            if now - self._last_sanity_error_time >= 1.0:
                                logger.warning("ingestion_sanity_check_failed", reason=res.errors[0].message)
                                self._last_sanity_error_time = now
                            continue
                            
                        await self._process_packet(packet)
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    logger.error("ingestion_service_error", error=str(e), exc_info=True)
                    await asyncio.sleep(0.1)
                finally:
                    self._queue.task_done()
        except asyncio.CancelledError:
            logger.info("ingestion_service_cancelled")
        finally:
            self._running = False

    async def _process_packet(self, packet: TelemetryPacket) -> None:
        """
        State machine and routing logic.
        """
        events = self._monitor.detect_events(packet)
        for event in events:
             if isinstance(event, RaceStarted):
                 logger.info("race_started", race_data=dataclasses.asdict(event)) 
             elif isinstance(event, RaceStopped):
                 logger.info("race_stopped", race_data=dataclasses.asdict(event))

        if packet.is_race_on == 1:
            accepted = self._out_queue.put_nowait(packet)
            if not accepted:
                logger.warning("out_queue_full_packet_dropped")
