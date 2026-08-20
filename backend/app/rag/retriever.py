from app.database.models import Chunk
from app.database.vector_store import VectorStore
from app.embeddings.base import BaseEmbedder


class Retriever:

    def __init__(
        self,
        embedder: BaseEmbedder,
        store: VectorStore,
    ):
        self.embedder = embedder
        self.store = store


    def retrieve(
        self,
        question: str,
        limit: int = 20,
    ) -> list[Chunk]:

        embedding = self.embedder.embed(question)

        return self.store.search(
            embedding=embedding,
            limit=limit,
        )