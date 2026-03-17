from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import get_settings

settings = get_settings()

# Main Database Engine
engine = create_async_engine(
    settings.db.connection_string.get_secret_value(),
    echo=settings.env == "development",
    future=True
)

# Main Database Session Factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db():
    """Dependency for providing database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize relational database tables."""
    from src.backend.database.relational import MainBase
    async with engine.begin() as conn:
        await conn.run_sync(MainBase.metadata.create_all)

async def init_telemetry_db():
    """Initialize telemetry database (TimescaleDB hypertable)."""
    from src.backend.database.models_telemetry import TSBase
    from sqlalchemy import text
    
    async with engine.begin() as conn:
        # 1. Create standard tables
        await conn.run_sync(TSBase.metadata.create_all)
        
        # 2. Convert telemetry to hypertable (only if not already converted)
        # TimescaleDB requires the 'time' column for hypertable
        await conn.execute(text("""
            SELECT create_hypertable('telemetry', 'time', if_not_exists => TRUE);
        """))

