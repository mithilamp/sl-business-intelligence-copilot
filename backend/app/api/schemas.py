from app.advisor.models import BusinessRecommendation
from app.land.models import LandBusinessReport
from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str
    conversation_id: int | None = None

class ChunkReference(BaseModel):
    chunk_index: int
    relevance_score: float

class SourceResponse(BaseModel):
    title: str
    filename: str
    source: str
    category: str | None = None
    document_type: str | None = None
    published_date: str | None = None
    document_url: str | None = None
    chunks: list[ChunkReference] | None = None

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]
    conversation_id: int

class BusinessAdviceRequest(BaseModel):
    question: str = Field(min_length=1)
    land_report: LandBusinessReport | None = None


class BusinessAdviceResponse(BaseModel):
    question: str
    recommendation: BusinessRecommendation
    sources: list[SourceResponse]
