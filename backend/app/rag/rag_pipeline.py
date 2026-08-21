from app.database.vector_store import VectorStore
from app.embeddings.base import BaseEmbedder
from app.embeddings.openai_embedder import OpenAIEmbedder
from app.llm.base import BaseLLM
from app.llm.openai_llm import OpenAILLM
from app.rag.context_builder import ContextBuilder
from app.prompts.rag import RAG_SYSTEM_PROMPT
from app.rag.models import RAGResults, Source
from app.database.models import Chunk

from app.memory.memory import ConversationMemory
from app.memory.context import MemoryContext
from app.memory.contextualizer import QuestionContextualizer

from app.rag.retriever import Retriever
from app.reranking.cross_encoder import CrossEncoderReranker
from app.core import langsmith
from langsmith import traceable

class RAGPipeline:

    def __init__(
            self,
            embedder: BaseEmbedder | None = None,
            store: VectorStore | None = None,
            llm: BaseLLM | None = None,
            context_builder: ContextBuilder | None = None,
            retriever: Retriever | None = None,
            reranker: CrossEncoderReranker | None = None,
            memory: ConversationMemory | None = None,
            contextualizer: QuestionContextualizer | None = None,
    ):

        self.embedder = embedder or OpenAIEmbedder()

        self.store = store or VectorStore()

        self.llm = llm or OpenAILLM()

        self.context_builder = context_builder or ContextBuilder()

        self.retriever = retriever or Retriever(
            embedder=self.embedder,
            store=self.store,
        )

        self.reranker = reranker or CrossEncoderReranker()

        self.memory = memory or ConversationMemory()

        self.memory_context = MemoryContext(self.memory)
        
        self.contextualizer = contextualizer or QuestionContextualizer(self.llm)

    @traceable(
        name="Retrieve Documents",
        run_type="retriever",
    )
    def retrieve(self, question: str) -> tuple[list[Chunk], str]:

        # First stage:
        # Vector similarity retrieves candidates
        candidates = self.retriever.retrieve(
            question,
            limit=20,
        )


        # Second stage:
        # Cross encoder reranks candidates
        reranked = self.reranker.rerank(
            question,
            candidates,
            top_k=5,
        )

        chunks = [item.chunk for item in reranked]

        context = self.context_builder.build(chunks)

        return chunks, context

    @traceable(
        name="RAG Pipeline",
        run_type="chain",
    )
    def ask(self, question: str, conversation_id: int | None = None) -> RAGResults:
        """
        Ask a question to the RAG pipeline and get an answer.
        """ 

        memory_context = ""

        contextualized_question = question

        # --------------------------------------------------
        # Conversation memory
        # --------------------------------------------------
        if conversation_id is not None:

            memory_context = self.memory_context.build(
                conversation_id=conversation_id,
            )

        if memory_context.strip():
            print("Conversation ID:", conversation_id)
            print("Memory context:", memory_context)
            contextualized_question = (
                self.contextualizer.contextualize(
                    question=question,
                    history=memory_context,
                )
            )

        # --------------------------------------------------
        # RAG retrieval + reranking
        # --------------------------------------------------
        chunks, context = self.retrieve(contextualized_question)

        user_prompt = f"""
            Conversation Context: {memory_context}

            Retrieved Context:{context}

            Question: {contextualized_question}
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

        # --------------------------------------------------
        # Save conversation
        # --------------------------------------------------
        if conversation_id is not None:

            self.memory.add_message(
                conversation_id=conversation_id,
                role="user",
                content=question,
            )

            self.memory.add_message(
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
            )

        return RAGResults(
            question=question,
            answer=answer,
            sources=sources
        )