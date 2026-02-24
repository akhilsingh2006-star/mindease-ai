from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  

from app.database import get_db
from app.schemas.stress import StressCreate, StressResponse
from app.services import stress_service

# used prefix here so don't have to type "/stress" on every route
router = APIRouter(
    prefix="/stress",
    tags=["Stress Analysis"]
)

# +++1. POST Endpoint (Analyzes and Saves) ---
@router.post("/", response_model=StressResponse)
def analyze_stress(stress_in: StressCreate, db: Session = Depends(get_db)):
    """
    Takes user text, analyzes the stress score via AI, and saves it to the database.
    """
    return stress_service.create_stress_entry(db=db, stress=stress_in)


# +++2. GET Endpoint (Fetches History) ---
@router.get("/{user_id}", response_model=List[StressResponse])
def get_stress_history(user_id: int, db: Session = Depends(get_db)):
    """
    Returns the stress history for a given user.
    """
    history = stress_service.get_user_stress_history(db=db, user_id=user_id)
    if not history:
        raise HTTPException(status_code=404, detail="No stress history found for this user")
    return history
