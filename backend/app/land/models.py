from typing import Any

from pydantic import BaseModel, Field


class LandBusinessAnalysis(BaseModel):

    observations: list[str] = Field(
        default_factory=list
    )

    opportunities: list[str] = Field(
        default_factory=list
    )

    risks: list[str] = Field(
        default_factory=list
    )

    requires_verification: list[str] = Field(
        default_factory=list
    )

    next_steps: list[str] = Field(
        default_factory=list
    )


class LandBusinessReport(BaseModel):
    """A source-separated, presentation-ready view of a land analysis."""

    report_version: str = "1.0"

    property_overview: dict[str, Any] = Field(default_factory=dict)

    location_and_accessibility: dict[str, Any] = Field(default_factory=dict)

    nearby_intelligence: dict[str, list[dict[str, Any]]] = Field(
        default_factory=dict
    )

    business_assessment: LandBusinessAnalysis = Field(
        default_factory=LandBusinessAnalysis
    )

    evidence_by_source: dict[str, Any] = Field(default_factory=dict)
