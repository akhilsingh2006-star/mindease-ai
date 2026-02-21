from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate

def create_user(db: Session, user: UserCreate) -> User:
    # Create the SQLAlchemy model instance
    db_user = User(name=user.name, email=user.email)
    
    # Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user