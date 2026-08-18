from app.database.postgres import Postgres
from app.database.models import Chunk

postgres = Postgres()

with postgres.get_session() as session:

    chunk = session.query(Chunk).first()

    print("Chunk:", chunk.chunk_index)
    print("Document:", chunk.document.title)
    print("Source:", chunk.document.source)
    print("Filename:", chunk.document.filename)