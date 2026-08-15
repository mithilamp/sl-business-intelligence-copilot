from app.database.vector_store import VectorStore
from app.embeddings.openai_embedder import OpenAIEmbedder
from app.rag.context_builder import ContextBuilder

embedder = OpenAIEmbedder()
store = VectorStore()
builder = ContextBuilder()

question = "What is the minimum capital requirement?"

embedding = embedder.embed(question)

chunks = store.search(
    embedding,
    limit=3,
)

context = builder.build(chunks)

print(context)