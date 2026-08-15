from app.database.vector_store import VectorStore
from app.embeddings.openai_embedder import OpenAIEmbedder

embedder = OpenAIEmbedder()
store = VectorStore()

question = "What is the minimum capital requirement for banks in Sri Lanka?"

embedding = embedder.embed(question)

results = store.search(embedding)

print(f"Retrieved {len(results)} chunks")

print("-" * 80)

first = results[0] if results else None

print(first.filename)
print(first.source)
print(first.chunk_index)

print("-" * 80)

print(first.text[:1000])