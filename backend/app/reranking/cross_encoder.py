from app.core.settings import settings
from app.reranking.models import RerankedChunk
from sentence_transformers import CrossEncoder

from app.database.models import Chunk
from app.reranking.base import BaseReranker


class CrossEncoderReranker(BaseReranker):

    def __init__(self):
        self.model = CrossEncoder(
            settings.RERANKER_MODEL
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
                Rank: {rank}
                Score: {score:.4f}
                File: {chunk.document.filename}
                Chunk: {chunk.chunk_index}

                {chunk.text[:500]}
                """
            )

        return [
            RerankedChunk(
                chunk=chunk,
                score=float(score),
            )
            for chunk, score in ranked[:top_k]
        ]