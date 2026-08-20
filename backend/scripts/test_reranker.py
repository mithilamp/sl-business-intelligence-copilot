from app.embeddings.openai_embedder import OpenAIEmbedder
from app.database.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.reranking.cross_encoder import CrossEncoderReranker


question = "What is the minimum capital requirement for opening a new bank?"

retriever = Retriever(
    embedder=OpenAIEmbedder(),
    store=VectorStore(),
)

chunks = retriever.retrieve(
    question,
    limit=10,
)

print(f"Retrieved candidates: {len(chunks)}")


reranker = CrossEncoderReranker()

reranked = reranker.rerank(
    question,
    chunks,
    top_k=5,
)


for i, chunk in enumerate(reranked):
    print("\n---", i)
    print(chunk.text[:300])