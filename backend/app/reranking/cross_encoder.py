from app.core.settings import settings
from app.reranking.models import RerankedChunk
from sentence_transformers import CrossEncoder

from app.database.models import Chunk
from app.reranking.base import BaseReranker
from langsmith import traceable

class CrossEncoderReranker(BaseReranker):

    def __init__(self):
        self.model = CrossEncoder(
            settings.RERANKER_MODEL
        )

    @traceable(
        name="Reranker",
        run_type="chain",
    )
    def rerank(
        self,
        question: str,
        chunks: list[Chunk],
        top_k: int = 5,
    ) -> list[RerankedChunk]:

        pairs = [
            (
                question,
                chunk.text,
            )
            for chunk in chunks
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(chunks, scores),
            key=lambda item: item[1],
            reverse=True,
        )

        for rank, (chunk, score) in enumerate(
            ranked[:top_k],
            start=1,
        ):
                print(
                    f"""
                ==============================
                RANK: {rank}
                SCORE: {score:.4f}

                FILE:
                {chunk.document.filename}

                CATEGORY:
                {chunk.document.category}

                TYPE:
                {chunk.document.document_type}

                CHUNK:
                {chunk.chunk_index}

                CONTENT:
                {chunk.text[:1000]}
                ==============================
                """
                )

        results = [
            RerankedChunk(
                chunk=chunk,
                score=float(score),
            )
            for chunk, score in ranked[:top_k]
        ]

        return results