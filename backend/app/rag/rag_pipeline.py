from app.database.vector_store import VectorStore
from app.embeddings.base import BaseEmbedder
from app.embeddings.openai_embedder import OpenAIEmbedder
from app.llm.base import BaseLLM
from app.llm.openai_llm import OpenAILLM
from app.rag.context_builder import ContextBuilder
from app.prompts.rag import RAG_SYSTEM_PROMPT
from app.rag.models import RAGResults


class RAGPipeline:

    def __init__(
            self, embedder: BaseEmbedder | None = None,
            store: VectorStore | None = None,
            llm: BaseLLM | None = None,
            context_builder: ContextBuilder | None = None
    ):
        self.embedder = embedder or OpenAIEmbedder()
        self.store = store or VectorStore()
        self.llm = llm or OpenAILLM()
        self.context_builder = context_builder or ContextBuilder()

    def ask(self, question: str) -> str:
        """
        Ask a question to the RAG pipeline and get an answer.
        """
        embedding = self.embedder.embed(question)

        chunks = self.store.search(embedding=embedding, limit=5)

        context = self.context_builder.build(chunks)

        user_prompt = f"""
            Context: {context}
            Question: {question}
        """
        answer = self.llm.generate(
            system_prompt=RAG_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        sources = sorted({chunk.filename for chunk in chunks})
        return RAGResults(
            question=question,
            answer=answer,
            sources=sources
        )