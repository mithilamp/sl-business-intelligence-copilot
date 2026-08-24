from typing import Any

from app.land.models import LandBusinessAnalysis, LandBusinessReport


class LandBusinessReportBuilder:
    """Build a report without adding facts beyond the available evidence."""

    DOCUMENT_FIELDS = (
        "property_boundaries",
        "dimensions",
        "area",
        "survey_numbers",
        "roads",
        "landmarks",
        "location_information",
        "notes",
    )

    GEOLOCATION_FIELDS = (
        "query",
        "matched_query",
        "found",
        "accuracy",
        "match_quality",
        "confidence",
        "source_confidence",
        "location_level",
        "coordinates",
        "address",
    )

    def build(self, analysis: dict[str, Any]) -> LandBusinessReport:
        geolocation = analysis.get("geolocation") or {}
        nearby = geolocation.get("nearby") or {}
        nearby_details = nearby.get("nearby_details") or {}
        business_assessment = LandBusinessAnalysis.model_validate(
            analysis.get("business_analysis") or {}
        )

        document_extracted = {
            field: analysis.get(field)
            for field in self.DOCUMENT_FIELDS
            if field in analysis
        }
        location_summary = {
            field: geolocation.get(field)
            for field in self.GEOLOCATION_FIELDS
            if field in geolocation
        }
        road_access = nearby_details.get("roads", [])

        return LandBusinessReport(
            property_overview={
                key: document_extracted[key]
                for key in (
                    "property_boundaries",
                    "dimensions",
                    "area",
                    "survey_numbers",
                    "notes",
                )
                if key in document_extracted
            },
            location_and_accessibility={
                "location_query": analysis.get("location_query"),
                "geolocation": location_summary or None,
                "nearby_status": nearby.get("status", "not_run"),
                "nearby_provider": nearby.get("provider"),
                "nearby_errors": nearby.get("errors", []),
                "document_roads": document_extracted.get("roads", []),
                "nearby_roads": road_access,
            },
            nearby_intelligence={
                category: nearby_details.get(category, [])
                for category in (
                    "schools",
                    "hospitals",
                    "businesses",
                    "banks",
                    "restaurants",
                    "hotels",
                )
            },
            business_assessment=business_assessment,
            evidence_by_source={
                "document_extracted": document_extracted,
                "external_geospatial": {
                    "geolocation": location_summary or None,
                    "nearby_intelligence": nearby_details,
                },
                "ai_inferences": business_assessment.model_dump(),
            },
        )
