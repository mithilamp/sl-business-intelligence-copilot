from pydantic import BaseModel, Field


class BusinessRecommendation(BaseModel):
    business_name: str

    summary: str

    suitability_score: float | None = Field(
        default=None,
        ge=0,
        le=10,
    )

    estimated_startup_cost: str | None = None

    break_even: str | None = None

    required_licenses: list[str] = Field(default_factory=list)

    top_risks: list[str] = Field(default_factory=list)

    next_steps: list[str] = Field(default_factory=list)

    supporting_sources: list[str] = Field(default_factory=list)