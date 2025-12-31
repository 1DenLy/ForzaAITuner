from pydantic import Field
from pydantic_settings import BaseSettings
from src.config import get_settings, Settings

class IngestionConfig(BaseSettings):
    """
    Configuration for the telemetry ingestion service.
    """
    UDP_PORT: int = Field(default=5300, description="UDP Port to listen on")
    BUFFER_SIZE: int = Field(default=60, description="Number of packets to buffer before flush")
    FLUSH_INTERVAL_SEC: float = Field(default=1.0, description="Time interval to flush buffer if not full")

    @property
    def global_settings(self) -> Settings:
        """
        Access to the global project settings.
        """
        return get_settings()
