"""Run the same benchmark against baseline and production retrieval."""

import json
from pathlib import Path
from typing import Any

from app.rag.rag_pipeline import RAGPipeline
from app.evaluation.answer_quality import AnswerQualityEvaluator


class RAGEvaluator:
    def __init__(
        self,
        pipeline: RAGPipeline | None = None,
        answer_evaluator: AnswerQualityEvaluator | None = None,
    ):
        self.pipeline = pipeline or RAGPipeline()
        self.answer_evaluator = answer_evaluator or AnswerQualityEvaluator()

    def load_questions(self) -> list[dict[str, Any]]:
        path = Path(__file__).parent / "datasets" / "benchmark_questions.json"
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def _source(chunk: Any, score: float | None, rank: int) -> dict[str, Any]:
        document = chunk.document
        return {"rank": rank, "score": round(float(score), 4) if score is not None else None,
                "title": document.title, "filename": document.filename, "source": document.source,
                "category": document.category, "document_type": document.document_type,
                "published_date": document.published_date, "document_url": document.document_url}

    @classmethod
    def _unique_sources(cls, ranked_chunks: list[tuple[Any, float | None]]) -> list[dict[str, Any]]:
        sources = []
        seen = set()
        for chunk, score in ranked_chunks:
            identity = chunk.document.id
            if identity in seen:
                continue
            seen.add(identity)
            sources.append(cls._source(chunk, score, len(sources) + 1))
            if len(sources) == 3:
                break
        return sources

    def run(
        self,
        include_answers: bool = False,
        grade_answers: bool = False,
    ) -> dict[str, list[dict[str, Any]]]:
        """Compare first-stage vector results with cross-encoder reranking."""
        baseline, production = [], []
        for item in self.load_questions():
            candidates = self.pipeline.retriever.retrieve(item["question"], limit=20)
            reranked = self.pipeline.reranker.rerank(item["question"], candidates, top_k=5)
            common = {key: item[key] for key in ("id", "question", "category", "expected_sources")}
            baseline.append({**common, "retrieved_sources": self._unique_sources([
                (chunk, None) for chunk in candidates
            ])})
            # The production pipeline reranks five chunks, takes its first three,
            # then presents unique documents in first-seen order.
            current = {**common, "retrieved_sources": self._unique_sources([
                (value.chunk, value.score) for value in reranked[:3]
            ])}
            if include_answers or grade_answers:
                current["answer"] = self.pipeline.ask(item["question"]).answer
            if grade_answers:
                context = self.pipeline.context_builder.build(
                    [value.chunk for value in reranked[:3]]
                )
                try:
                    current["answer_quality"] = self.answer_evaluator.grade(
                        question=item["question"],
                        answer=current["answer"],
                        context=context,
                    ).model_dump()
                except Exception as exc:
                    # Preserve a judge-format failure without losing the run.
                    current["answer_quality_error"] = f"{type(exc).__name__}: {exc}"
            production.append(current)
        return {"vector_only": baseline, "vector_plus_reranker": production}
