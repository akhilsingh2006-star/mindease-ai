from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from app.database import Base


class StressLog(Base):
    __tablename__ = "stress_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    note = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
