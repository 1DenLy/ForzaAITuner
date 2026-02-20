import asyncio
import logging
import threading
from typing import Optional

from src.presentation.interfaces.protocols import ICoreFacade
from .ingestion_service import IngestionService
from .packet_parser import PacketParser
from ..infrastructure.udp_transport import UdpListener
from src.config import get_settings

# Setup logger for this module
logger = logging.getLogger(__name__)

class RealCoreFacade(ICoreFacade):
    """
    Concrete implementation of the ICoreFacade.
    
    Orchestrates the actual Forza Core components (IngestionService, UDP listener).
    It uses a standalone Event Loop running in a dedicated background thread to
    prevent blocking the UI and properly isolate asyncio paradigms from standard threads.
    """
    
    def __init__(self, out_queue: asyncio.Queue):
        """
        Receives out_queue from UI.
        Internally creates UDP queue, listener, parser and ingestion service.
        """
        self._out_queue = out_queue
        self._is_running = False
        
        # Dedicated Event Loop Thread for I/O and asyncio operations
        self._loop = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self._loop_thread.start()
        
        self._ingestion_task: Optional[asyncio.Task] = None
        self._udp_transport: Optional[asyncio.DatagramTransport] = None
        
        # Load settings for network config
        self._settings = get_settings()

    def _run_event_loop(self) -> None:
        """Runs the asyncio event loop in a dedicated background thread."""
        logger.info("Core asyncio event loop thread started.")
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
        finally:
            self._loop.close()
            logger.info("Core asyncio event loop thread stopped.")

    def start_tracking(self) -> None:
        if self._is_running:
            logger.warning("Attempted to start tracking while already running.")
            return

        logger.info("Starting Core Tracking...")
        self._is_running = True
        
        # Schedule the coroutine in the background event loop
        asyncio.run_coroutine_threadsafe(self._start_async(), self._loop)

    async def _start_async(self) -> None:
        """Starts the ingestion service inside the event loop via asyncio.create_task and creates UDP endpoint."""
        # 1. Create internal UDP queue
        udp_queue = asyncio.Queue(maxsize=1000)
        
        # 2. Composition: initialize dependencies
        parser = PacketParser()
        self._ingestion_service = IngestionService(
            queue=udp_queue,
            out_queue=self._out_queue,
            parser=parser
        )
        
        # 3. Start ingestion task
        self._ingestion_task = self._loop.create_task(self._ingestion_service.run())
        logger.info("IngestionService task created and running.")
        
        # 4. Create UDP Endpoint
        try:
            transport, protocol = await self._loop.create_datagram_endpoint(
                lambda: UdpListener(udp_queue),
                local_addr=(self._settings.network.host, self._settings.network.port)
            )
            self._udp_transport = transport
            logger.info(f"UDP Transport started listening on {self._udp_transport.get_extra_info('sockname')}.")
        except Exception as e:
            logger.error(f"Failed to start UDP transport: {e}")

    def stop_tracking(self) -> None:
        if not self._is_running:
            return

        logger.info("Stopping Core Tracking...")
        self._is_running = False
        
        future = asyncio.run_coroutine_threadsafe(self._stop_async(), self._loop)
        try:
            # Thread-safe stopping mechanism with a time limit
            future.result(timeout=2.0)
            logger.info("Core Tracking Stopped.")
        except Exception as e:
            logger.error(f"Error stopping Core Tracking: {e}")

    async def _stop_async(self) -> None:
        """Safely stops running background tasks within the event loop."""
        if self._udp_transport and not self._udp_transport.is_closing():
            self._udp_transport.close()
            logger.info("UDP Transport closed.")

        if self._ingestion_task and not self._ingestion_task.done():
            self._ingestion_task.cancel()
            try:
                await asyncio.wait_for(self._ingestion_task, timeout=2.0)
            except asyncio.TimeoutError:
                logger.warning("Ingestion task cancellation timed out (2.0s).")
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.error(f"Error during ingestion task cancellation: {e}")
            finally:
                self._ingestion_task = None

    def cleanup(self) -> None:
        logger.info("Cleaning up Core resources...")
        self.stop_tracking()
        self._loop.call_soon_threadsafe(self._loop.stop)
        if self._loop_thread.is_alive():
            self._loop_thread.join(timeout=2.0)

    def is_tracking(self) -> bool:
        return self._is_running
