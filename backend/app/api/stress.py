from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.stress import StressLog 

router = APIRouter()

@router.post("/stress")
def create_stress_entry(level: int,note: str ="",db:Session = Depends(get_db)):
    new_entry=StressLog(
        level=level,
        note=note
    )
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)


    return {
        "message":"Stress entry saved successfully",
        "data":{
            "id":new_entry.id,
            "level":new_entry.level,
            "note":new_entry.note
        }
    }