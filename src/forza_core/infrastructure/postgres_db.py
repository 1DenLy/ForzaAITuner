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

