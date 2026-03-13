import asyncio
import logging
from typing import Optional, Callable

from desktop_client.domain.interface.interfaces import IOutQueue, IAsyncRunner, IPacketParser, ICoreFacade
from .ingestion_service import IngestionService


# Setup logger for this module
logger = logging.getLogger(__name__)

class RealCoreFacade(ICoreFacade):
    """
    Concrete implementation of the ICoreFacade.
    
    Orchestrates the actual Forza Core components (IngestionService, UDP listener).
    It uses an injected IAsyncRunner to execute async ingestion tasks.
    """
    
    def __init__(self, 
                 out_queue: IOutQueue, 
                 async_runner: IAsyncRunner,
                 packet_parser: IPacketParser,
                 ingestion_factory: Callable[[asyncio.Queue, IOutQueue, IPacketParser], IngestionService],
                 udp_protocol_factory: Callable[[asyncio.Queue], asyncio.DatagramProtocol],
                 host: str,
                 port: int):
        """
        Receives dependencies from Composition Root.
        """
        self._out_queue = out_queue
        self._async_runner = async_runner
        self._packet_parser = packet_parser
        self._ingestion_factory = ingestion_factory
        self._udp_protocol_factory = udp_protocol_factory
        self._host = host
        self._port = port
        
        self._is_running = False
        
        # Start async runner thread if not already running
        self._async_runner.start()
        
        self._ingestion_task: Optional[asyncio.Task] = None
        self._udp_transport: Optional[asyncio.DatagramTransport] = None
        


    def start_tracking(self) -> None:
        if self._is_running:
            logger.warning("Attempted to start tracking while already running.")
            return

        logger.info("Starting Core Tracking...")
        self._is_running = True
        
        # Schedule the coroutine in the background event loop
        self._async_runner.submit(self._start_async())

    async def _start_async(self) -> None:
        """Starts the ingestion service inside the event loop via asyncio.create_task and creates UDP endpoint."""
        loop = asyncio.get_running_loop()
        # 1. Create internal UDP queue
        udp_queue = asyncio.Queue(maxsize=1000)
        
        # 2. Composition: inject dependencies into ingestion service via factory
        self._ingestion_service = self._ingestion_factory(udp_queue, self._out_queue, self._packet_parser)
        
        # 3. Start ingestion task
        self._ingestion_task = loop.create_task(self._ingestion_service.run())
        logger.info("IngestionService task created and running.")
        
        # 4. Create UDP Endpoint
        try:
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: self._udp_protocol_factory(udp_queue),
                local_addr=(self._host, self._port)
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
        
        future = self._async_runner.submit(self._stop_async())
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
        self._async_runner.stop()

    def is_tracking(self) -> bool:
        return self._is_running
