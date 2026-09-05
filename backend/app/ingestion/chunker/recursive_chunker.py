from app.core.logger import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ingestion.chunker.base import BaseChunker

class RecursiveChunker(BaseChunker):

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def chunk(self, text: str) -> list[str]:
        logger.info(f"Chunking document ({len(text)} characters)")
        chunks = self.splitter.split_text(text)
        logger.info(f"Created {len(chunks)} chunks")
        return chunks