from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..application.ingestion_service import IngestionService
from .schemas import SessionStartRequest, OperationResponse
import structlog

logger = structlog.get_logger()

def create_app(ingestion_service: IngestionService) -> FastAPI:
    """
    Factory to create FastAPI app with injected dependencies.
    """
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup logic if needed
        logger.info("api_startup")
        yield
        # Shutdown logic if needed
        logger.info("api_shutdown")

    app = FastAPI(lifespan=lifespan)

    @app.post("/session/start", response_model=OperationResponse)
    async def start_session(request: SessionStartRequest):
        logger.info("api_start_session", **request.model_dump())
        await ingestion_service.set_session(
            car_ordinal=request.car_id,
            track_id=request.track_id, 
            tuning_config_id=request.tuning_config_id
        )
        return OperationResponse(status="success", message="Session started")

    @app.post("/session/stop", response_model=OperationResponse)
    async def stop_session():
        logger.info("api_stop_session")
        await ingestion_service.stop_session()
        return OperationResponse(status="success", message="Session stopped")

    return app
