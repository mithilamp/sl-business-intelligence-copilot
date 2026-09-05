from app.advisor.business_advisor import BusinessAdvisor
from fastapi import APIRouter
from app.agents.land_agent import LandAgent
from app.land.vision import LandVisionResponseError
from fastapi import UploadFile, File, HTTPException
from pathlib import Path

from app.api.schemas import (
    AgentRequest,
    AgentResponse,
    BusinessAdviceRequest,
    BusinessAdviceResponse,
    ConversationDetailResponse,
    ConversationListItem,
    ConversationMessageResponse,
    QuestionRequest,
    QuestionResponse,
    SourceResponse,
)
from app.agents.router import AgentRouter
from app.rag.rag_pipeline import RAGPipeline

router = APIRouter()
pipeline = RAGPipeline()
agent_router = AgentRouter(pipeline=pipeline)


def conversation_title(conversation) -> str:
    if conversation.title:
        return conversation.title

    messages = pipeline.memory.get_recent_messages(
        conversation_id=conversation.id,
        limit=100,
    )
    first_question = next(
        (message.content for message in messages if message.role == "user"),
        None,
    )
    return first_question[:255] if first_question else "Untitled conversation"


@router.post(
    "/ask",
    response_model=QuestionResponse,
)

def ask(request: QuestionRequest):

    conversation_id = request.conversation_id

    if conversation_id is None:
        conversation = pipeline.memory.create_conversation(
            title=request.question.strip()[:255]
        )
        conversation_id = conversation.id

    result = pipeline.ask(request.question, conversation_id=conversation_id)
    sources = [
    SourceResponse(
        title=source.title,
        filename=source.filename,
        source=source.source,
        category=source.category,
        document_type=source.document_type,
        published_date=source.published_date,
        document_url=source.document_url,
        chunks=source.chunks,
    )
        for source in result.sources
    ]

    return QuestionResponse(
        question=result.question,
        answer=result.answer,
        sources=sources,
        conversation_id=conversation_id
    )


@router.post("/agent", response_model=AgentResponse)
def agent(request: AgentRequest):
    conversation_id = request.conversation_id
    if conversation_id is None:
        conversation = pipeline.memory.create_conversation(
            title=request.question.strip()[:255]
        )
        conversation_id = conversation.id

    result = agent_router.run(
        question=request.question,
        conversation_id=conversation_id,
        land_report=request.land_report,
    )
    return AgentResponse(
        question=result.question,
        answer=result.answer,
        sources=[
            SourceResponse(
                title=source.title,
                filename=source.filename,
                source=source.source,
                category=source.category,
                document_type=source.document_type,
                published_date=source.published_date,
                document_url=source.document_url,
                chunks=source.chunks,
            )
            for source in result.sources
        ],
        selected_tool=result.tool,
        routing_reason=result.reason,
        conversation_id=result.conversation_id,
    )


@router.get(
    "/conversations",
    response_model=list[ConversationListItem],
)
def conversations():
    return [
        ConversationListItem(
            id=conversation.id,
            title=conversation_title(conversation),
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )
        for conversation in pipeline.memory.list_conversations()
    ]


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationDetailResponse,
)
def conversation_detail(conversation_id: int):
    conversation = pipeline.memory.get_conversation(conversation_id)

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    messages = pipeline.memory.get_recent_messages(
        conversation_id=conversation_id,
        limit=100,
    )

    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation_title(conversation),
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[
            ConversationMessageResponse(
                id=message.id,
                role=message.role,
                content=message.content,
                created_at=message.created_at,
            )
            for message in messages
        ],
    )

@router.post(
    "/business-advice",
    response_model=BusinessAdviceResponse,
)
def business_advice(request: BusinessAdviceRequest):

    advisor = BusinessAdvisor()

    result = advisor.recommend(
        request.question,
        land_report=request.land_report,
    )

    sources_map = {}


    for item in result.chunks:

        chunk = item.chunk
        document = chunk.document


        if document.id not in sources_map:

            sources_map[document.id] = SourceResponse(
                title=document.title,
                filename=document.filename,
                source=document.source,
                category=document.category,
                document_type=document.document_type,
                published_date=document.published_date,
                document_url=document.document_url,
                chunks=[]
            )


        sources_map[document.id].chunks.append(
            {
                "chunk_index": chunk.chunk_index,
                "relevance_score": round(
                    float(item.score),
                    4
                )
            }
        )

    sources = list(sources_map.values())


    return BusinessAdviceResponse(
        question=request.question,
        recommendation=result.recommendation,
        sources=sources,
    )

@router.post("/land-analysis")
def land_analysis(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, JPEG and PNG files are supported."
        )


    BASE_DIR = Path(__file__).resolve().parents[2]

    upload_dir = BASE_DIR / "data" / "uploads"

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = upload_dir / file.filename


    with open(file_path, "wb") as buffer:
        buffer.write(
            file.file.read()
        )


    agent = LandAgent()

    try:
        result = agent.analyze(
            str(file_path)
        )
    except LandVisionResponseError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    return result
