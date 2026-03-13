from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, delete
from database.models import Session

class SessionRepository:
    """
    Repository handling Session data across two separate databases (MainDB for relations, TSDB for telemetry).
    """
    
    @staticmethod
    async def delete_session(session_id: int, main_db: AsyncSession, ts_db: AsyncSession):
        """
        Deletes a session and its associated telemetry manually via a software cascade, 
        avoiding cross-database foreign key constraints.
        
        This prevents OOM errors on large deletes by avoiding loading ORM objects into memory.
        """
        # 1. First, delete all telemetry for this session from the TSDB
        # Using raw SQL or SQLAlchemy core on the TSDB schema
        try:
            await ts_db.execute(
                text("DELETE FROM telemetry WHERE session_id = :session_id"),
                {"session_id": session_id}
            )
            await ts_db.commit()
            
            # 2. Delete the session from the PostgreSQL Main database
            await main_db.execute(
                delete(Session).where(Session.id == session_id)
            )
            await main_db.commit()
            
        except Exception as e:
            await ts_db.rollback()
            await main_db.rollback()
            raise e
