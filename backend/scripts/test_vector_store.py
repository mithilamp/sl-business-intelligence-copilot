from pathlib import Path

from app.database.vector_store import VectorStore
from app.ingestion.chunker.recursive_chunker import RecursiveChunker
from app.ingestion.parser.pdf_parser import PDFParser
from app.embeddings.openai_embedder import OpenAIEmbedder

parser = PDFParser()
chunker = RecursiveChunker()
embedder = OpenAIEmbedder()
store = VectorStore()

text = parser.parse(
    Path("../data/raw/central_bank/banks.pdf")
)

chunks = chunker.chunk(text)

embedding = embedder.embed(chunks[0])

store.add(
    source="CBSL",
    filename="banks.pdf",
    chunk_index=0,
    text=chunks[0],
    embedding=embedding,
)

print("Done!")