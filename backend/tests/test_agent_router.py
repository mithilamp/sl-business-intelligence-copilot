from unittest.mock import Mock

from app.agents.router import AgentDecision, AgentRouter
from app.rag.models import RAGResults


def _router(decision: AgentDecision):
    pipeline = Mock()
    pipeline.memory_context.build.return_value = ""
    pipeline.llm = Mock()
    llm = Mock()
    llm.generate_structured.return_value = decision
    advisor = Mock()
    router = AgentRouter(pipeline=pipeline, llm=llm, advisor=advisor)
    return router, pipeline, advisor


def test_agent_model_selects_knowledge_search_and_records_memory():
    router, pipeline, _ = _router(
        AgentDecision(tool="knowledge_search", reason="Needs official evidence")
    )
    router.rag_agent.run = Mock(
        return_value=RAGResults(question="Q", answer="Grounded answer", sources=[])
    )

    result = router.run("What sectors are promoted?", conversation_id=7)

    assert result.tool == "knowledge_search"
    assert result.answer == "Grounded answer"
    router.rag_agent.run.assert_called_once_with("What sectors are promoted?")
    assert pipeline.memory.add_message.call_count == 2


def test_agent_model_selects_advisor_with_land_report():
    router, _, advisor = _router(
        AgentDecision(tool="business_advisor", reason="Feasibility recommendation")
    )
    recommendation = Mock()
    recommendation.model_dump_json.return_value = '{"summary":"Review access"}'
    advisor.recommend.return_value.recommendation = recommendation
    report = {"property_overview": {}, "business_assessment": {}, "evidence_by_source": {}}

    result = router.run("Is tourism suitable?", conversation_id=9, land_report=report)

    assert result.tool == "business_advisor"
    advisor.recommend.assert_called_once_with("Is tourism suitable?", land_report=report)
    assert "Review access" in result.answer


def test_agent_uses_history_to_contextualize_follow_up():
    router, pipeline, _ = _router(
        AgentDecision(tool="knowledge_search", reason="Follow-up research")
    )
    pipeline.memory_context.build.return_value = "User asked about exports"
    pipeline.contextualizer.contextualize.return_value = "Which export incentives apply?"
    router.rag_agent.run = Mock(
        return_value=RAGResults(question="Q", answer="Answer", sources=[])
    )

    router.run("Which incentives?", conversation_id=3)

    pipeline.contextualizer.contextualize.assert_called_once()
    router.rag_agent.run.assert_called_once_with("Which export incentives apply?")
