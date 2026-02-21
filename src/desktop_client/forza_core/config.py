from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class IngestionConfig(BaseSettings):
    """
    Configuration for the telemetry ingestion service.
    Focuses on application-level settings (buffering, logic).
    Network and DB settings are handled by the global configuration.
    """
    model_config = SettingsConfigDict(
        env_prefix="INGESTION_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
