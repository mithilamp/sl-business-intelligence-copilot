from typing import Literal

from langsmith import traceable
from pydantic import BaseModel, Field

from app.advisor.business_advisor import BusinessAdvisor
from app.agents.rag_agent import RAGAgent
from app.land.models import LandBusinessReport
from app.llm.base import BaseLLM
from app.llm.openai_llm import OpenAILLM
from app.rag.rag_pipeline import RAGPipeline


class AgentDecision(BaseModel):
    tool: Literal["knowledge_search", "business_advisor"]
    reason: str = Field(description="A short explanation of why this tool is appropriate.")


class AgentResult(BaseModel):
    tool: Literal["knowledge_search", "business_advisor"]
    reason: str
    question: str
    answer: str
    conversation_id: int


class AgentRouter:

    SYSTEM_PROMPT = """You route a Sri Lanka business question to exactly one tool.

Available tools:
- knowledge_search: factual or explanatory questions that should be answered from the document collection.
- business_advisor: recommendations, comparisons, action plans, feasibility questions, or questions that include a land report.

Use the conversation history to resolve follow-up intent. Choose business_advisor whenever a land report is supplied. Return only the structured decision."""

    def __init__(
        self,
        pipeline: RAGPipeline | None = None,
        llm: BaseLLM | None = None,
        advisor: BusinessAdvisor | None = None,
    ):
        self.pipeline = pipeline or RAGPipeline()
        self.llm = llm or OpenAILLM()
        self.rag_agent = RAGAgent(self.pipeline)
        self.business_advisor = advisor or BusinessAdvisor(
            rag=self.pipeline,
            llm=self.pipeline.llm,
        )

    @traceable(name="Choose Agent Tool", run_type="llm", tags=["agent", "routing"])
    def choose_tool(
        self,
        question: str,
        history: str,
        has_land_report: bool,
    ) -> AgentDecision:
        return self.llm.generate_structured(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=(
                f"Conversation history:\n{history or 'None'}\n\n"
                f"Land report supplied: {has_land_report}\n\nQuestion:\n{question}"
            ),
            response_model=AgentDecision,
        )

    @traceable(name="Business Copilot Agent", run_type="chain", tags=["agent", "memory"])
    def run(
        self,
        question: str,
        conversation_id: int,
        land_report: LandBusinessReport | None = None,
    ) -> AgentResult:
        history = self.pipeline.memory_context.build(conversation_id=conversation_id)
        contextualized_question = question
        if history.strip():
            contextualized_question = self.pipeline.contextualizer.contextualize(
                question=question,
                history=history,
            )

        decision = self.choose_tool(
            question=contextualized_question,
            history=history,
            has_land_report=land_report is not None,
        )

        if decision.tool == "business_advisor":
            result = self.business_advisor.recommend(
                contextualized_question,
                land_report=land_report,
            )
            answer = result.recommendation.model_dump_json(indent=2)
        else:
            answer = self.rag_agent.run(contextualized_question).answer

        self.pipeline.memory.add_message(conversation_id, "user", question)
        self.pipeline.memory.add_message(conversation_id, "assistant", answer)

        return AgentResult(
            tool=decision.tool,
            reason=decision.reason,
            question=question,
            answer=answer,
            conversation_id=conversation_id,
        )
