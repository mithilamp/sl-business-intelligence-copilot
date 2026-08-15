from fastapi import APIRouter

from app.api.schemas import QuestionRequest, QuestionResponse
from app.rag.rag_pipeline import RAGPipeline

router = APIRouter()
pipeline = RAGPipeline()


@router.post(
    "/ask",
    response_model=QuestionResponse,
)

def ask(request: QuestionRequest):
    result = pipeline.ask(request.question)
    return QuestionResponse(
        question=result.question,
        answer=result.answer,
        sources=result.sources
    )