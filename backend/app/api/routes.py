from app.advisor.business_advisor import BusinessAdvisor
from fastapi import APIRouter

from app.api.schemas import BusinessAdviceRequest, BusinessAdviceResponse, QuestionRequest, QuestionResponse, SourceResponse
from app.rag.rag_pipeline import RAGPipeline

router = APIRouter()
pipeline = RAGPipeline()


@router.post(
    "/ask",
    response_model=QuestionResponse,
)

def ask(request: QuestionRequest):

    conversation_id = request.conversation_id

    if conversation_id is None:
        conversation = pipeline.memory.create_conversation()
        conversation_id = conversation.id

    result = pipeline.ask(request.question, conversation_id=request.conversation_id)
    sources = [
    SourceResponse(
        title=source.title,
        filename=source.filename,
        source=source.source,
        category=source.category,
        document_type=source.document_type,
        published_date=source.published_date,
        document_url=source.document_url,
    )
        for source in result.sources
    ]

    return QuestionResponse(
        question=result.question,
        answer=result.answer,
        sources=sources,
        conversation_id=conversation_id
    )

@router.post(
    "/business-advice",
    response_model=BusinessAdviceResponse,
)
def business_advice(request: BusinessAdviceRequest):

    advisor = BusinessAdvisor()

    result = advisor.recommend(request.question)

    sources = list({
        chunk.document.id: SourceResponse(
            title=chunk.document.title,
            filename=chunk.document.filename,
            source=chunk.document.source,
            category=chunk.document.category,
            document_type=chunk.document.document_type,
            published_date=chunk.document.published_date,
            document_url=chunk.document.document_url,
        )
        for chunk in result.chunks
    }.values())

    return BusinessAdviceResponse(
        question=request.question,
        recommendation=result.recommendation,
        sources=sources,
    )