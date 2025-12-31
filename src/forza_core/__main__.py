import asyncio
import sys
import signal
import structlog
from typing import Set

from .config import IngestionConfig
from .infrastructure.logging import setup_logging
from .infrastructure.postgres_db import PostgresRepository
from .infrastructure.udp_transport import UdpListener
from .application.ingestion_service import IngestionService
import asyncpg

logger = structlog.get_logger()

async def main():
    # 1. Platform Check & uvloop
    if sys.platform != 'win32':
        try:
            import uvloop
            uvloop.install()
            logger.info("uvloop_installed")
        except ImportError:
            pass

    # 2. Config
    config = IngestionConfig()

    # 3. Logging
    setup_logging(config.global_settings.env)
    
    logger.info("service_starting", env=config.global_settings.env, port=config.UDP_PORT)

    # 4. DI Container
    queue = asyncio.Queue(maxsize=10000)

    # Database Pool
    # We use global settings for DB DSN
    try:
        pool = await asyncpg.create_pool(
            dsn=config.global_settings.db.connection_string.replace("+asyncpg", "") # asyncpg doesn't like the schema prefix sometimes if passed as dsn directly? 
            # pydantic PostgresDsn might have schema. 
            # Actually asyncpg dsn is usually just postgresql://...
            # config.global_settings.db.connection_string is "postgresql+asyncpg://..." which is for SQLAlchemy.
            # We need to strip "+asyncpg".
        )
    except Exception as e:
        logger.critical("db_connection_failed", error=str(e))
        sys.exit(1)

    repo = PostgresRepository(pool)
    service = IngestionService(repo, config, queue)
    transport = UdpListener(queue)

    loop = asyncio.get_running_loop()
    
    # Signals
    stop_event = asyncio.Event()

    def signal_handler():
        logger.info("shutdown_signal_received")
        stop_event.set()

    # Register signals
    if sys.platform != 'win32':
        loop.add_signal_handler(signal.SIGTERM, signal_handler)
        loop.add_signal_handler(signal.SIGINT, signal_handler)
    else:
        # Windows doesn't support add_signal_handler for SIGTERM/INT nicely in loop sometimes or needs different handling
        # But for basics, we rely on ensure_future or standard exception if KeyboardInterrupt
        pass

    # 5. Tasks
    try:
        # We use TaskGroup in 3.11+, assume we have it in 3.12
        async with asyncio.TaskGroup() as tg:
            # Task 1: UDP Server
            # create_datagram_endpoint return (transport, protocol)
            # We wrap it in a task to keep it alive? No, generic create_datagram_endpoint runs in background on loop
            # But we need to keep the loop running.
            
            udp_coro = loop.create_datagram_endpoint(
                lambda: transport,
                local_addr=("0.0.0.0", config.UDP_PORT)
            )
            
            udp_task = tg.create_task(udp_coro)
            
            # Task 2: Service Worker
            service_task = tg.create_task(service.run())
            
            # Task 3: Watchdog (Optional) - skipping for simplicity as per spec optional
            
            # Wait for stop signal
            if sys.platform == 'win32':
                 # Windows fallback for signal handling
                while not stop_event.is_set():
                    try:
                        await asyncio.sleep(1)
                    except asyncio.CancelledError:
                        stop_event.set()
            else:
                await stop_event.wait()
            
            # Graceful Shutdown
            logger.info("shutdown_initiated")
            
            # Stop UDP reception
            # udp_task result is (transport, protocol)
            # extract transport to close it
            # But udp_task is a Task that awaits the creation.
            # The creation returns immediately.
            # Wait, create_datagram_endpoint returns (transport, protocol).
            # We should await it once.
            
            # Actually, `tg` waits for all tasks. `udp_task` finishes when endpoint is created?
            # Creating endpoint is fast. We need to keep the reference.
            
    except* Exception as e: # ExceptionGroup
         logger.error("fatal_error", error=str(e))

    finally:
        # Shutdown logic
        logger.info("cleanup_started")
        
        # We need access to the transport object created by create_datagram_endpoint
        # But I put it in a task which returns it.
        # Refactoring to run create_datagram_endpoint before TaskGroup or await it inside.
        pass

# Refactoring main to handle cleanup properly outside TaskGroup or careful usage
async def main_refactored():
    # ... setup code ...
    if sys.platform != 'win32':
        try:
            import uvloop
            uvloop.install()
        except ImportError: pass
        
    config = IngestionConfig()
    setup_logging(config.global_settings.env)
    
    queue = asyncio.Queue(maxsize=10000)
    
    try:
        dsn = config.global_settings.db.connection_string.replace("+asyncpg", "")
        pool = await asyncpg.create_pool(dsn)
    except Exception as e:
        logger.critical("db_connection_failed", error=str(e))
        return

    repo = PostgresRepository(pool)
    service = IngestionService(repo, config, queue)
    transport_proto = UdpListener(queue)
    
    loop = asyncio.get_running_loop()
    
    # Start UDP
    try:
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: transport_proto,
            local_addr=("0.0.0.0", config.UDP_PORT)
        )
        logger.info("udp_server_started", port=config.UDP_PORT)
    except Exception as e:
        logger.critical("udp_bind_failed", error=str(e))
        await pool.close()
        return

    # To handle signals elegantly on Windows and Linux + TaskGroup
    stop_event = asyncio.Event()
    
    def stop():
        if not stop_event.is_set():
            logger.info("stopping_service")
            stop_event.set()

    if sys.platform != 'win32':
        loop.add_signal_handler(signal.SIGTERM, stop)
        loop.add_signal_handler(signal.SIGINT, stop)
        
    # Service Task
    service_task = asyncio.create_task(service.run())
    
    try:
        # Run until stop event or KeyboardInterrupt
        if sys.platform == 'win32':
            # Windows signal hack
            while not stop_event.is_set():
                await asyncio.sleep(0.5)
        else:
            await stop_event.wait()
            
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        stop()
    
    # Graceful Shutdown
    transport.close()
    logger.info("udp_transport_closed")
    
    # Wait for queue to drain? 
    # Spec: "Дождаться обработки очереди (queue.join())"
    # But queue might confuse consumers if we don't stop them?
    # Service loop checks `_running`.
    # We should signal service to stop BUT after queue is empty?
    # Or we let it consume.
    
    # If we stop UDP, no new packets.
    # Service is still running.
    # await queue.join() blocks until all items are processed.
    logger.info("waiting_for_queue_drain")
    
    # We can't await queue.join() if the consumer is the one calling task_done() and we are blocking here.
    # We are in main. The consumer is in service_task.
    # So queue.join() is fine.
    
    # But if the queue is empty, join returns immediately.
    # If it has items, we wait.
    try:
        await asyncio.wait_for(queue.join(), timeout=5.0)
    except asyncio.TimeoutError:
        logger.warning("queue_drain_timeout")

    # Now stop the service
    service_task.cancel()
    try:
        await service_task
    except asyncio.CancelledError:
        pass
        
    # Final flush
    await service.flush()
    
    await pool.close()
    logger.info("shutdown_complete")

if __name__ == "__main__":
    try:
        asyncio.run(main_refactored())
    except KeyboardInterrupt:
        pass
