from app.database.vector_store import VectorStore
from app.embeddings.base import BaseEmbedder
from app.embeddings.openai_embedder import OpenAIEmbedder
from app.llm.base import BaseLLM
from app.llm.openai_llm import OpenAILLM
from app.rag.context_builder import ContextBuilder
from app.prompts.rag import RAG_SYSTEM_PROMPT
from app.rag.models import RAGResults, Source
from app.database.models import Chunk


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

    def retrieve(self, question: str) -> tuple[list[Chunk], str]:
        """
        Retrieve relevant chunks from the vector store based on the question.
        """
        embedding = self.embedder.embed(question)
        chunks = self.store.search(embedding=embedding, limit=5)
        context = self.context_builder.build(chunks)
        return chunks, context

    def ask(self, question: str) -> RAGResults:
        """
        Ask a question to the RAG pipeline and get an answer.
        """
        chunks, context = self.retrieve(question)

        user_prompt = f"""
            Context: {context}
            Question: {question}
        """
        answer = self.llm.generate(
            system_prompt=RAG_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )


        sources = []
        seen_documents = set()

        for chunk in chunks:
            document = chunk.document

            if document.id not in seen_documents:
                sources.append(
                    Source(
                        title=document.title,
                        filename=document.filename,
                        source=document.source,
                        document_url=document.document_url,
                    )
                )
                seen_documents.add(document.id)

        return RAGResults(
            question=question,
            answer=answer,
            sources=sources
        )