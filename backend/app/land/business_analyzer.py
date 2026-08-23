from app.llm.base import BaseLLM
from app.llm.openai_llm import OpenAILLM
from app.prompts.land_business import LAND_BUSINESS_PROMPT
from app.land.models import LandBusinessAnalysis


class LandBusinessAnalyzer:

    def __init__(
        self,
        llm: BaseLLM | None = None,
    ):
        self.llm = llm or OpenAILLM()

    def analyze(
        self,
        land_data: dict,
    ):

        prompt = f"""
Land intelligence data:

{land_data}

Analyze this property from a business-intelligence perspective.
Use only information contained in the supplied land intelligence.

Identify:

1. Key factual observations
2. Potential business opportunities suggested by the data
3. Potential constraints or risks
4. Factors that require further verification
5. Recommended next steps

Do not invent:
- property measurements
- prices
- regulations
- licenses
- businesses
- nearby facilities
- market demand
- financial estimates

If information is unavailable, explicitly say that it is unavailable.

Return the result as structured JSON.
"""

        return self.llm.generate_structured(
            system_prompt=LAND_BUSINESS_PROMPT,
            user_prompt=prompt,
            response_model=LandBusinessAnalysis,
        )