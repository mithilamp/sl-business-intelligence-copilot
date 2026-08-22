from sqlalchemy.orm import joinedload

from app.core.logger import logger
from app.database.postgres import Postgres
from app.database.models import Chunk, Document

class VectorStore:
    def __init__(self, postgres: Postgres | None = None):
        self.postgres = postgres or Postgres()

    def add(
            self,
            document_id: int,
            chunk_index: int,
            text: str,
            embedding: list[float],
    ):
        session = self.postgres.get_session()
        try:
            chunk = Chunk(
                document_id=document_id,
                chunk_index=chunk_index,
                text=text,
                embedding=embedding,
            )
            session.add(chunk)
            session.commit()
            logger.info(f"Stored chunk {chunk_index} from {document_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error storing chunk {chunk_index} from {document_id}: {e}")
            raise
        finally:
            session.close()


    def search(self, embedding: list[float], limit: int = 5) -> list[Chunk]:
        session = self.postgres.get_session()
        try:
            results: list[Chunk] = (
                session.query(Chunk)
                .options(joinedload(Chunk.document))
                .order_by(Chunk.embedding.cosine_distance(embedding))
                .limit(limit)
                .all()
            )
            logger.info(f"Retrieved {len(results)} chunks (limit={limit}).")
            print("NUMBER OF VECTOR RESULTS:", len(results))
            return results
        except Exception:
            logger.error("Failed to search vector store.")
            raise
        finally:
            session.close()


    def get_or_create_document(
        self,
        title: str,
        filename: str,
        source: str,
        document_url: str | None = None,
        category: str | None = None,
        document_type: str | None = None,
        published_date: str | None = None,
        language: str | None = None,
    ) -> Document:

        session = self.postgres.get_session()

        try:
            document = (
                session.query(Document)
                .filter(Document.filename == filename)
                .first()
            )

            if document:

                document.document_url = document_url
                document.category = category
                document.document_type = document_type
                document.published_date = published_date
                document.language = language

                session.commit()

                session.refresh(document)

                return document

            document = Document(
                title=title,
                filename=filename,
                source=source,
                document_url=document_url,
                category=category,
                document_type=document_type,
                published_date=published_date,
                language=language,
            )

            session.add(document)
            session.commit()
            session.refresh(document)

            logger.info(
                f"Created document: {filename} "
                f"(id={document.id})"
            )

            return document

        except Exception:
            session.rollback()
            logger.error(
                f"Failed to create/find document: {filename}"
            )
            raise

        finally:
            session.close()

    def has_chunks(self, document_id: int) -> bool:
        session = self.postgres.get_session()

        try:
            return (
                session.query(Chunk)
                .filter(Chunk.document_id == document_id)
                .first()
                is not None
            )

        finally:
            session.close()