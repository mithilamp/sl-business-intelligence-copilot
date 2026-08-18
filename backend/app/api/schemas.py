from app.advisor.models import BusinessRecommendation
from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str

class SourceResponse(BaseModel):
    title: str
    filename: str
    source: str
    document_url: str | None = None

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]

class BusinessAdviceRequest(BaseModel):
    question: str = Field(min_length=1)


class BusinessAdviceResponse(BaseModel):
    question: str
    recommendation: BusinessRecommendation
    sources: list[SourceResponse]