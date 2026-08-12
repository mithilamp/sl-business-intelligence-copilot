from pathlib import Path

from app.ingestion.parser.pdf_parser import PDFParser
from app.ingestion.chunker.recursive_chunker import RecursiveChunker

parser = PDFParser()
chunker = RecursiveChunker()

text = parser.parse(
    Path("../data/raw/central_bank/banks.pdf")
)

chunks = chunker.chunk(text)

print(f"Chunks: {len(chunks)}")
print("-" * 80)
print(chunks[0])
print(f"First chunk length: {len(chunks[0])}")