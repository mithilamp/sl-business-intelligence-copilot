"""Structured LLM grading for end-to-end answer quality."""

from statistics import mean
from typing import Any

from langsmith import traceable
from pydantic import BaseModel, Field

from app.llm.base import BaseLLM
from app.llm.openai_llm import OpenAILLM


class AnswerQualityGrade(BaseModel):
    groundedness: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)
    citation_quality: int = Field(ge=1, le=5)
    unsupported_claims: list[str] = Field(default_factory=list)
    failure_analysis: str


class AnswerQualityEvaluator:
    SYSTEM_PROMPT = """You are a strict evaluator of a retrieval-grounded answer.
Score each dimension from 1 (poor) to 5 (excellent).

- groundedness: substantive claims are supported by the supplied retrieved context.
- relevance: the answer directly addresses the question and avoids irrelevant detail.
- citation_quality: source references are identifiable and connected to claims.

List every unsupported substantive claim you can identify. Do not reward fluency. If the context is insufficient, score groundedness conservatively and explain the failure."""

    def __init__(self, llm: BaseLLM | None = None):
        self.llm = llm or OpenAILLM()

    @traceable(name="Grade Answer Quality", run_type="llm", tags=["evaluation", "groundedness"])
    def grade(self, question: str, answer: str, context: str) -> AnswerQualityGrade:
        return self.llm.generate_structured(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=f"QUESTION:\n{question}\n\nRETRIEVED CONTEXT:\n{context}\n\nANSWER:\n{answer}",
            response_model=AnswerQualityGrade,
        )


def summarise_answer_quality(results: list[dict[str, Any]]) -> dict[str, Any]:
    grades = [item["answer_quality"] for item in results if item.get("answer_quality")]
    if not grades:
        return {"graded_answers": 0, "status": "not_run"}
    return {
        "graded_answers": len(grades),
        "mean_groundedness_1_to_5": round(mean(g["groundedness"] for g in grades), 3),
        "mean_relevance_1_to_5": round(mean(g["relevance"] for g in grades), 3),
        "mean_citation_quality_1_to_5": round(mean(g["citation_quality"] for g in grades), 3),
        "answers_with_unsupported_claims": sum(bool(g["unsupported_claims"]) for g in grades),
        "status": "llm_judge_review_required",
    }
