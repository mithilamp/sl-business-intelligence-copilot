from abc import ABC, abstractmethod
from app.database.models import Chunk


class BaseReranker(ABC):

    @abstractmethod
    def rerank(
        self,
        question: str,
        chunks: list[Chunk],
        top_k: int = 5,
    ) -> list[Chunk]:
        pass