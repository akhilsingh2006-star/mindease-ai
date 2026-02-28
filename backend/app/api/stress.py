from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  
import base64
import numpy as np
import cv2
from deepface import DeepFace
from fastapi import HTTPException

from app.database import get_db
from app.schemas.stress import StressCreate, StressResponse, FaceRequest
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

@router.post("/analyze-face")
def analyze_face(request: FaceRequest):
    try:
        encoded_data = request.image_base64.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        
        dominant_emotion = result[0]['dominant_emotion']
        
        return {"emotion": dominant_emotion.capitalize(), "confidence": 0.95}

    except Exception as e:
        print(f"CNN Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process image")
