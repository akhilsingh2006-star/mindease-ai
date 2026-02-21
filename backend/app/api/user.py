from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.dependencies import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db=db, user=user_data)
        return new_user
    except IntegrityError:
        # This catches the error if someone tries to use an email that already exists
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")