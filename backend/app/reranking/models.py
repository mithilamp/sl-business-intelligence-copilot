from dataclasses import dataclass

from app.database.models import Chunk


@dataclass
class RerankedChunk:
    chunk: Chunk
    score: float