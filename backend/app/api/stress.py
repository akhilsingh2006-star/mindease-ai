from typing import List
import fastapi
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.stress import StressCreate
from app.services.stress_service import create_stress_entry

router = fastapi.APIRouter()

@router.post("/stress")
def create_stress(stress_data: StressCreate, db: Session = fastapi.Depends(get_db)):
    # Pass the heavy lifting to the service layer!
    new_entry = create_stress_entry(db=db, stress=stress_data)
    
    return {
        "message": "Stress entry saved successfully",
        "data": {
            "id": new_entry.id,
            "user_id": new_entry.user_id,
            "stress_score": new_entry.stress_score
        }
    }