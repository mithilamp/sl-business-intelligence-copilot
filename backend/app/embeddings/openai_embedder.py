from app.core.logger import logger
from openai import OpenAI

from app.core.settings import settings
from app.embeddings.base import BaseEmbedder

class OpenAIEmbedder(BaseEmbedder):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def embed(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""
        logger.info("Generating embedding...")
        response = self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=text
        )
        logger.info("Embedding created.")
        return response.data[0].embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        response = self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=texts
        )
        logger.info(f"Generated {len(texts)} embeddings.")
        return [item.embedding for item in response.data]