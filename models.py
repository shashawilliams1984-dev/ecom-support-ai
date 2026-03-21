from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

# Request schema (for API input)
class QuestionRequest(BaseModel):
    question: str

# Database model
class QuestionDB(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
