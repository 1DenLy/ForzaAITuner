from enum import Enum
from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel, Field, SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


#  Working modes
class AppEnvironment(str, Enum):
    """Working modes"""
    DEV = "development"
    PROD = "production"
    TEST = "testing"


#  UDP network config
class NetworkConfig(BaseModel):
    """UDP network config"""
    host: str = Field(default="0.0.0.0", description="IP address to bind")
    port: int = Field(default=5300, description="Forza UDP Port")


#  Database config
class DatabaseConfig(BaseModel):
    """Database config"""
    host: str = Field(..., description="Database host")
    port: int = Field(..., description="Database port")
    user: str = Field(..., description="Database user")

    password: SecretStr = Field(..., description="Database password")
    name: str = Field(..., description="Database name")

    @property
    def connection_string(self) -> str:
        """URL for connection SQLAlchemy/asyncpg"""
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


#  AI config
class AIConfig(BaseModel):
    """AI config"""
    model_path: Path = Field(
        default=Path("src/models/v1_tuner.onnx"),
        description="Path to ONNX model file"
    )
    enable_inference: bool = Field(default=True, description="Enable AI inference")
    device: str = Field(default="cpu", description="Inference device (cpu/cuda)")


#  Main Settings
class Settings(BaseSettings):
    """
    Main Settings class.
    Reads configuration from .env file or environment variables.
    """
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="_",
        extra = "ignore"
    )

    env: AppEnvironment = Field(default=AppEnvironment.DEV, alias="APP_ENV")

    # Compose configs
    network: NetworkConfig = Field(default_factory=NetworkConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    ai: AIConfig = Field(default_factory=AIConfig)


@lru_cache
def get_settings() -> Settings:
    """
    Creates and returns a (cached) instance of settings.
    Used for Dependency Injection.
    """
    return Settings()