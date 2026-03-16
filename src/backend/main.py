import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.backend.database.db import get_db, engine
from src.backend.database.models import MainBase, Car, Tune

app = FastAPI(
    title="Forza AI Tuner Backend",
    description="API for Forza Horizon 5 AI Tuning and Telemetry",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    # In development, we might want to create tables automatically 
    # if not using Alembic yet.
    async with engine.begin() as conn:
        # Note: This creates tables for the MainBase. 
        # For TSBase (Telemetry), manual creation or Alembic is better.
        await conn.run_sync(MainBase.metadata.create_all)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "backend"}

@app.get("/api/cars")
async def get_cars(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Car))
    cars = result.scalars().all()
    return cars

@app.post("/api/tunes")
async def create_tune(tune_data: dict, db: AsyncSession = Depends(get_db)):
    # Basic skeleton for saving a tune
    # In a real app, we would use Pydantic models to validate tune_data
    return {"message": "Tune saving logic to be implemented", "received": tune_data}

if __name__ == "__main__":
    uvicorn.run("src.backend.main:app", host="0.0.0.0", port=8000, reload=True)
