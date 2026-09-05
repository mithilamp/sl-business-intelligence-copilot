from unittest.mock import Mock

from app.advisor.business_advisor import BusinessAdvisor
from app.advisor.models import BusinessRecommendation
from app.api.schemas import BusinessAdviceRequest
from app.land.context_builder import LandContextBuilder


def _land_report():
    return {
        "property_overview": {"area": {"value": "20 perches"}},
        "business_assessment": {
            "requires_verification": ["Confirm legal access"],
        },
        "evidence_by_source": {
            "document_extracted": {
                "area": {"value": "20 perches"},
                "roads": [],
            },
            "external_geospatial": {
                "geolocation": {
                    "confidence": "low",
                    "address": "Example, Sri Lanka",
                },
            },
            "ai_inferences": {
                "opportunities": ["Possible tourism use"],
                "requires_verification": ["Confirm legal access"],
            },
        },
    }


def test_land_context_preserves_provenance_and_removes_empty_values():
    context = LandContextBuilder().build(_land_report())

    assert '"document_extracted"' in context
    assert '"external_geospatial"' in context
    assert '"ai_inferences"' in context
    assert '"confidence": "low"' in context
    assert '"verification_requirements"' in context
    assert '"roads"' not in context


def test_advisor_adds_optional_land_context_without_changing_rag_sources():
    rag = Mock()
    rag.retrieve.return_value = ([], "Policy evidence from RAG")
    llm = Mock()
    llm.generate_structured.return_value = BusinessRecommendation(
        business_name="Proposed venture",
        summary="Verification is required.",
    )
    advisor = BusinessAdvisor(rag=rag, llm=llm)

    result = advisor.recommend("Is this suitable?", land_report=_land_report())

    prompt = llm.generate_structured.call_args.kwargs["user_prompt"]
    assert "RAG DOCUMENT EVIDENCE:\nPolicy evidence from RAG" in prompt
    assert "LAND REPORT EVIDENCE:" in prompt
    assert '"document_extracted"' in prompt
    assert result.chunks == []
    assert result.recommendation.supporting_sources == []


def test_business_advice_request_accepts_land_report_or_omits_it():
    with_land = BusinessAdviceRequest(
        question="Is this suitable?",
        land_report=_land_report(),
    )
    without_land = BusinessAdviceRequest(question="What should I consider?")

    assert with_land.land_report is not None
    assert without_land.land_report is None
