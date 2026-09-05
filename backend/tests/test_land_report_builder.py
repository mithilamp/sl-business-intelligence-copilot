from app.land.report_builder import LandBusinessReportBuilder


def test_report_keeps_evidence_sources_separate_and_preserves_distances():
    analysis = {
        "area": {"value": "20 perches"},
        "survey_numbers": ["SP-1"],
        "roads": ["Document road reference"],
        "location_query": {"search_query": "Example village", "confidence": "medium"},
        "geolocation": {
            "found": True,
            "accuracy": "fallback",
            "match_quality": "local",
            "confidence": "medium",
            "coordinates": {"latitude": 6.9, "longitude": 79.8},
            "nearby": {
                "nearby_details": {
                    "schools": [{"name": "A School", "distance_meters": 250}],
                    "roads": [{"name": "A1", "distance_meters": 100}],
                }
            },
        },
        "business_analysis": {
            "observations": ["Observed from supplied data"],
            "opportunities": [],
            "risks": [],
            "requires_verification": ["Confirm legal access"],
            "next_steps": ["Inspect the site"],
        },
    }

    report = LandBusinessReportBuilder().build(analysis).model_dump()

    assert report["property_overview"]["area"] == {"value": "20 perches"}
    assert report["location_and_accessibility"]["nearby_roads"][0]["distance_meters"] == 100
    assert report["nearby_intelligence"]["schools"][0]["distance_meters"] == 250
    assert report["evidence_by_source"]["document_extracted"]["survey_numbers"] == ["SP-1"]
    assert report["evidence_by_source"]["ai_inferences"]["next_steps"] == ["Inspect the site"]


def test_report_is_available_when_geolocation_is_missing():
    report = LandBusinessReportBuilder().build({"notes": ["Unclear scan"]})

    assert report.location_and_accessibility["geolocation"] is None
    assert report.business_assessment.requires_verification == []
    assert report.evidence_by_source["document_extracted"]["notes"] == ["Unclear scan"]
