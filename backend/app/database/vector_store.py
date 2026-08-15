from app.core.logger import logger
from app.database.postgres import Postgres
from app.database.models import Chunk

class VectorStore:
    def __init__(self, postgres: Postgres | None = None):
        self.postgres = postgres or Postgres()

    def add(
            self,
            source: str,
            filename: str,
            chunk_index: int,
            text: str,
            embedding: list[float],
    ):
        session = self.postgres.get_session()
        try:
            chunk = Chunk(
                source=source,
                filename=filename,
                chunk_index=chunk_index,
                text=text,
                embedding=embedding,
            )
            session.add(chunk)
            session.commit()
            logger.info(f"Stored chunk {chunk_index} from {filename}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error storing chunk {chunk_index} from {filename}: {e}")
            raise
        finally:
            session.close()


    def search(self, embedding: list[float], limit: int = 5) -> list[Chunk]:
        session = self.postgres.get_session()
        try:
            results: list[Chunk] = (
                session.query(Chunk)
                .order_by(Chunk.embedding.cosine_distance(embedding))
                .limit(limit)
                .all()
            )
            logger.info(f"Retrieved {len(results)} chunks (limit={limit}).")
            return results
        except Exception:
            logger.error("Failed to search vector store.")
            raise
        finally:
            session.close()