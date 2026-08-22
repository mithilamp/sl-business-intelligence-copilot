from app.advisor.models import BusinessRecommendation
from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str
    conversation_id: int | None = None

class SourceResponse(BaseModel):
    title: str
    filename: str
    source: str
    category: str | None = None
    document_type: str | None = None
    published_date: str | None = None
    document_url: str | None = None
    chunks: list[dict] | None = None

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]
    conversation_id: int

class BusinessAdviceRequest(BaseModel):
    question: str = Field(min_length=1)


class BusinessAdviceResponse(BaseModel):
    question: str
    recommendation: BusinessRecommendation
    sources: list[SourceResponse]