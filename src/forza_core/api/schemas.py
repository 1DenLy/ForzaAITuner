from pydantic import BaseModel
from typing import Optional

class SessionStartRequest(BaseModel):
    car_id: int
    track_id: str
    tuning_config_id: Optional[int] = None

class OperationResponse(BaseModel):
    status: str
    message: str