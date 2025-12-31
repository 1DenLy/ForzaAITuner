import asyncpg
import dataclasses
from typing import List
from ..domain.interfaces import ITelemetryRepository
from ..domain.models import TelemetryPacket

class PostgresRepository(ITelemetryRepository):
    """
    PostgreSQL implementation of telemetry repository using COPY for speed.
    """
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def save_batch(self, packets: List[TelemetryPacket]) -> None:
        if not packets:
            return

        # Prepare list of tuples
        # We rely on packets being frozen and slots, so astuple is fast enough?
        # dataclasses.astuple might be slow for 60Hz * Buffer.
        # Faster is list comprehension with manual field access if needed, but astuple is cleaner.
        # Let's verify requirement: "Использовать connection.copy_records_to_table"
        
        # We need to ensure the columns match the packet fields order.
        # Assuming table 'telemetry_data' (or similar) with columns matching TelemetryPacket fields.
        
        # Performance trick: compiled retrieval if needed, but for now astuple is fine for 60 items.
        
        values = [dataclasses.astuple(p) for p in packets]
        
        async with self._pool.acquire() as conn:
            # Get field names from the dataclass to ensure correct column matching if we were generating SQL,
            # but copy_records_to_table usually takes positional args or columns list.
            # We should probably specify columns to be safe.
            columns = [f.name for f in dataclasses.fields(TelemetryPacket)]
            
            await conn.copy_records_to_table(
                'telemetry_packets', # Table name assumption!
                records=values,
                columns=columns,
                timeout=10
            )

