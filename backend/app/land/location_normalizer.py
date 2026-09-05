import json

from app.llm.base import BaseLLM


class LocationNormalizer:

    def __init__(
        self,
        llm: BaseLLM,
    ):
        self.llm = llm


    def normalize(
        self,
        locations: list[str],
    ) -> dict:

        prompt = f"""
You are a geographic information extraction assistant.

A land survey document was analyzed by a vision model.
The extracted location information may contain:
- legal descriptions
- lot references
- survey terminology
- administrative divisions

Your task:
Create the best possible query for a geocoding service.

Rules:
- Remove lot numbers
- Remove survey/legal descriptions
- Do not invent locations
- Keep only geographic entities
- Prefer village -> district -> province -> country
- If uncertain, reflect uncertainty in confidence

Extracted location information:

{locations}


Return ONLY JSON:

{{
    "search_query": "",
    "confidence": "high|medium|low"
}}
"""

        response = self.llm.generate(
            system_prompt=(
                "You normalize noisy geographic information "
                "for geolocation systems."
            ),
            user_prompt=prompt,
        )


        return json.loads(response)