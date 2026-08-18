from app.advisor.models import BusinessRecommendation
from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]

class BusinessAdviceRequest(BaseModel):
    question: str = Field(min_length=1)


class BusinessAdviceResponse(BaseModel):
    question: str
    recommendation: BusinessRecommendation
    sources: list[str]