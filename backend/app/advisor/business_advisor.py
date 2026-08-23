from dataclasses import dataclass
from typing import Any

from app.llm.base import BaseLLM
from app.land.context_builder import LandContextBuilder
from app.land.models import LandBusinessReport
from app.prompts.business_advisor import BUSINESS_ADVISOR_PROMPT
from app.advisor.models import BusinessRecommendation
from app.rag.rag_pipeline import RAGPipeline
from app.reranking.models import RerankedChunk


@dataclass
class BusinessAdviceResult:
    recommendation: BusinessRecommendation
    chunks: list[RerankedChunk]


class BusinessAdvisor:

    def __init__(
        self,
        rag: RAGPipeline | None = None,
        llm: BaseLLM | None = None,
        land_context_builder: LandContextBuilder | None = None,
    ):
        self.rag = rag or RAGPipeline()
        self.llm = llm or self.rag.llm
        self.land_context_builder = land_context_builder or LandContextBuilder()

    def recommend(
        self,
        question: str,
        land_report: LandBusinessReport | dict[str, Any] | None = None,
    ) -> BusinessAdviceResult:

        chunks, context = self.rag.retrieve(question)

        land_context = (
            self.land_context_builder.build(land_report)
            if land_report is not None
            else "Not provided"
        )

        user_prompt = f"""RAG DOCUMENT EVIDENCE:
{context or "Not available"}

LAND REPORT EVIDENCE:
{land_context}

BUSINESS QUESTION:
{question}
"""

        recommendation = self.llm.generate_structured(
            system_prompt=BUSINESS_ADVISOR_PROMPT,
            user_prompt=user_prompt,
            response_model=BusinessRecommendation,
        )

        recommendation.supporting_sources = sorted({
            item.chunk.document.filename
            for item in chunks
        })

        return BusinessAdviceResult(
            recommendation=recommendation,
            chunks=chunks,
        )
