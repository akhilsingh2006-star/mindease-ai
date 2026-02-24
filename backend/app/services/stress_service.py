from sqlalchemy.orm import Session
from app.models.stress import StressLog
from app.schemas.stress import StressCreate

from app.ml.stress_model.predict import predict_stress_level

def create_stress_entry(db: Session, stress: StressCreate) -> StressLog:
    
    # 1. AI calculates the score based on the note
    ai_calculated_score = predict_stress_level(stress.note)

    # 2. Save the entry using the AI's score
    new_entry = StressLog(
        stress_score=ai_calculated_score,  # Fix 3: Use the AI's score!
        user_id=stress.user_id,            # Fix 1: Added the missing comma here
        note=stress.note                   # Fix 2: Corrected to stress.note
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

def get_user_stress_history(db: Session, user_id: int):
    """
    Fetches all stress logs for a specific user, ordered by newest first.
    """
    return db.query(StressLog).filter(StressLog.user_id == user_id).order_by(StressLog.id.desc()).all()
