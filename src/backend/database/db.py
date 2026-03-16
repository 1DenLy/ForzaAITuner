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
