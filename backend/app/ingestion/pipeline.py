from pathlib import Path

from app.core.logger import logger
from app.core.sources import DataSource
from app.database.vector_store import VectorStore
from app.embeddings.openai_embedder import OpenAIEmbedder
from app.ingestion.chunker.recursive_chunker import RecursiveChunker
from app.ingestion.parser.pdf_parser import PDFParser

class IngestionPipeline:

    def __init__(self):

        self.parser = PDFParser()

        self.chunker = RecursiveChunker()

        self.embedder = OpenAIEmbedder()

        self.store = VectorStore()


    def ingest_pdf(self, source: DataSource, pdf_path: Path):

        logger.info(f"Ingesting {pdf_path.name} from source {source.name}")

        document = self.store.get_or_create_document(
            title=pdf_path.stem.replace("_", " ").title(),
            filename=pdf_path.name,
            source=source.name,
        )

        if self.store.has_chunks(document.id):
            logger.info(f"Document already has chunks.Skipping ingestion: {pdf_path.name}")
            return

        text = self.parser.parse(pdf_path)

        chunks = self.chunker.chunk(text)

        for index, chunk in enumerate(chunks):
            embedding = self.embedder.embed(chunk)

            self.store.add(
                document_id=document.id,
                chunk_index=index,
                text=chunk,
                embedding=embedding,
            )
        logger.info(f"Finished ingesting {pdf_path.name}")