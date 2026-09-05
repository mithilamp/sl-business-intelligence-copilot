from app.llm.base import BaseLLM
from langsmith import traceable

CONTEXTUALIZER_PROMPT = """
You are a question contextualizer for a business intelligence
RAG system.

Your job is to rewrite the user's latest question into a
standalone question that can be understood without the
conversation history.

Rules:

1. Preserve the user's original intent.
2. Use information from the conversation only when necessary
   to resolve references such as:
   - "it"
   - "they"
   - "that"
   - "the foreign one"
   - "what about..."
3. Do not answer the question.
4. Do not add information that is not supported by the
   conversation.
5. If the question is already standalone, return it unchanged.
6. Return ONLY the rewritten question.
7. Do not introduce new facts.
8. Do not change the scope of the question.
9. Only resolve references using information explicitly present
   in the conversation.
10. Keep the rewritten question as close as possible to the
    original question.
"""


class QuestionContextualizer:

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    @traceable(
        name="Question Contextualizer",
        run_type="chain",
    )
    def contextualize(self, question: str, history: str,) -> str:

        if not history.strip():
            return question

        user_prompt = f"""
        Conversation history:

        {history}

        Latest user question:

        {question}

        Rewrite the latest question as a standalone question.
        """

        return self.llm.generate(
            system_prompt=CONTEXTUALIZER_PROMPT,
            user_prompt=user_prompt,
        ).strip()