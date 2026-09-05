import json
from typing import Any

from app.land.models import LandBusinessReport


class LandContextBuilder:
    """Format a land report for the advisor without adding new claims."""

    def build(
        self,
        land_report: LandBusinessReport | dict[str, Any],
    ) -> str:
        report = (
            land_report
            if isinstance(land_report, LandBusinessReport)
            else LandBusinessReport.model_validate(land_report)
        )

        evidence = self._remove_empty(report.evidence_by_source)
        verification_items = self._remove_empty(
            report.business_assessment.requires_verification
        )

        payload: dict[str, Any] = {
            "report_version": report.report_version,
            "evidence_by_source": evidence,
        }
        if verification_items:
            payload["verification_requirements"] = verification_items

        return json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )

    def _remove_empty(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: cleaned
                for key, item in value.items()
                if (cleaned := self._remove_empty(item)) not in (None, "", [], {})
            }
        if isinstance(value, list):
            return [
                cleaned
                for item in value
                if (cleaned := self._remove_empty(item)) not in (None, "", [], {})
            ]
        return value
