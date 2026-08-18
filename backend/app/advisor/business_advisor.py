from app.llm.base import BaseLLM
from app.prompts.business_advisor import BUSINESS_ADVISOR_PROMPT
from app.advisor.models import BusinessRecommendation
from app.rag.rag_pipeline import RAGPipeline

class BusinessAdvisor:

    def __init__(self, rag: RAGPipeline | None = None,llm: BaseLLM | None = None):
        self.rag = rag or RAGPipeline()
        self.llm = llm or self.rag.llm

    def recommend(
            self,
            question: str,
    ) -> BusinessRecommendation:

        chunks, context = self.rag.retrieve(question)

        user_prompt = f"""
        Context:
        {context}

        Business Question:
        {question}
        """

        recommendation = self.llm.generate_structured(
            system_prompt=BUSINESS_ADVISOR_PROMPT,
            user_prompt=user_prompt,
            response_model=BusinessRecommendation
        )

        recommendation.supporting_sources = sorted({
            chunk.filename
            for chunk in chunks
        })

        return recommendation