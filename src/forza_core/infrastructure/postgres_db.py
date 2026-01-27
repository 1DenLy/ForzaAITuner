import asyncpg
import dataclasses
from typing import List
from ..domain.interfaces import ITelemetryRepository
from ..domain.models import TelemetryPacket

class PostgresRepository(ITelemetryRepository):
    """
    PostgreSQL implementation of telemetry repository using COPY for speed.
    """
    def __init__(self, pool: asyncpg.Pool, table_name: str = "telemetry_packets"):
        self._pool = pool
        self._table_name = table_name

    async def save_batch(self, packets: List[TelemetryPacket]) -> None:
        if not packets:
            return

        # Prepare list of tuples
        # Prepare generator of tuples for performance (avoiding astuple introspection overhead)
        # Note: We must ensure field order matches!
        values = (dataclasses.astuple(p) for p in packets)
        
        async with self._pool.acquire() as conn:
            columns = [f.name for f in dataclasses.fields(TelemetryPacket)]
            
            await conn.copy_records_to_table(
                self._table_name,
                records=values,
                columns=columns,
                timeout=10
            )

    async def create_session(self, car_ordinal: int, track_id: str, tuning_config_id: int | None = None) -> int:
        query = """
            INSERT INTO sessions (car_ordinal, track_id, tuning_config_id)
            VALUES ($1, $2, $3)
            RETURNING id
        """
        async with self._pool.acquire() as conn:
            # Assuming 'sessions' table exists. If not, this will fail at runtime, 
            # but per instructions we assume structure.
            session_id = await conn.fetchval(query, car_ordinal, track_id, tuning_config_id)
            return session_id

