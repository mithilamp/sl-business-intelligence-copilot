from app.advisor.business_advisor import BusinessAdvisor
from fastapi import APIRouter

from app.api.schemas import BusinessAdviceRequest, BusinessAdviceResponse, QuestionRequest, QuestionResponse
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

@router.post(
    "/business-advice",
    response_model=BusinessAdviceResponse,
)
def business_advice(request: BusinessAdviceRequest):
    advisor = BusinessAdvisor()
    recommendation = advisor.recommend(request.question)
    return BusinessAdviceResponse(
        question=request.question,
        recommendation=recommendation,
        sources=recommendation.supporting_sources)