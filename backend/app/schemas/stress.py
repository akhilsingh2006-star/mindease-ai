from pydantic import BaseModel, Field
from typing import Optional

class StressCreate(BaseModel):
    user_id: int
    stress_score: Optional[int] = 0 #Optional because the API will overwrite it
    note: str 


class StressResponse(BaseModel):
    id: int
    stress_score: float
    user_id: int
    note: str

    class Config:
        from_attributes = True