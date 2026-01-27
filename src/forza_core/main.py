import asyncio
import sys
import structlog
import uvicorn
from ..config import IngestionConfig
from ..infrastructure.logging import setup_logging
from ..infrastructure.postgres_db import PostgresRepository
from ..infrastructure.udp_transport import UdpListener
from ..application.ingestion_service import IngestionService
from ..application.packet_parser import PacketParser
from .api.server import create_app
import asyncpg
from src.config import get_settings

logger = structlog.get_logger()

async def main():
    if sys.platform != 'win32':
        try:
            import uvloop
            uvloop.install()
        except ImportError: pass
        
    global_settings = get_settings()
    ingestion_config = IngestionConfig()
    
    setup_logging(global_settings.env)
    
    queue = asyncio.Queue(maxsize=10000)
    
    try:
        dsn = global_settings.db.get_asyncpg_dsn().get_secret_value()
        pool = await asyncpg.create_pool(dsn)
    except Exception as e:
        logger.critical("db_connection_failed", error=str(e))
        return


    repo = PostgresRepository(pool)
    parser = PacketParser()
    service = IngestionService(repo, ingestion_config, queue, parser)
    transport_proto = UdpListener(queue)
    
    loop = asyncio.get_running_loop()
    
    # 1. Start UDP Transport
    try:
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: transport_proto,
            local_addr=(global_settings.network.host, global_settings.network.port)
        )
        logger.info("udp_server_started", port=global_settings.network.port)
    except Exception as e:
        logger.critical("udp_bind_failed", error=str(e))
        await pool.close()
        return

    # 2. Background Ingestion Task
    ingestion_task = asyncio.create_task(service.run())
    
    # 3. HTTP Server (API)
    api_app = create_app(service)
    http_config = uvicorn.Config(api_app, host="0.0.0.0", port=8000, log_level="info")
    http_server = uvicorn.Server(http_config)
    
    logger.info("api_server_starting", port=8000)
    
    try:
        # Run HTTP server - this blocks until shutdown signal
        await http_server.serve()
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("shutdown_initiated")
        
        # Cleanup
        transport.close()
        
        # Cancel ingestion service
        ingestion_task.cancel()
        try:
            await ingestion_task
        except asyncio.CancelledError:
            pass
            
        # Final flush
        await service.flush()
        
        await pool.close()
        logger.info("shutdown_complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
