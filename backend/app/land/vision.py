from openai import OpenAI
import base64

from app.core.settings import settings


class LandVisionResponseError(RuntimeError):
    """Raised when the vision model does not return usable JSON."""


class LandVisionAnalyzer:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )


    def analyze(
        self,
        image_path: str,
    ):

        with open(image_path, "rb") as image_file:

            encoded_image = base64.b64encode(
                image_file.read()
            ).decode("utf-8")


        response = self.client.chat.completions.create(

            model="gpt-4o",

            messages=[

                {
                    "role": "system",
                    "content": """
You are a land survey analysis assistant.

Analyze the attached land survey plan image.

Return ONLY valid JSON.
No markdown.
No explanations.

Extract:

{
 "property_boundaries": [],
 "dimensions": {},
 "area": {},
 "survey_numbers": [],
 "roads": [],
 "landmarks": [],
 "location_information": [],
 "notes": []
}
"""
                },

                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this land survey plan."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            }
                        }
                    ]
                }

            ],

            response_format={"type": "json_object"},
            max_tokens=1500,
        )


        choice = response.choices[0]
        result = choice.message.content

        if not result or not result.strip():
            refusal = getattr(choice.message, "refusal", None)
            detail = refusal or f"finish reason: {choice.finish_reason}"
            raise LandVisionResponseError(
                f"The vision model returned no land-analysis JSON ({detail})."
            )

        print("VISION RESPONSE:")
        print(result)

        return result
