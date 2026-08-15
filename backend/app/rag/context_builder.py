from app.database.models import Chunk

class ContextBuilder:

    def build(self, chunks: list[Chunk]) -> str:
        """
        Build a context string from a list of chunks.
        """
        separator = "\n\n" + "=" * 80 + "\n\n"
        parts = []

        for chunk in chunks:
            parts.append(
                f"""Source: {chunk.source}
                File: {chunk.filename}
                Chunk: {chunk.chunk_index}

                {chunk.text}"""
            )
        return separator.join(parts)  