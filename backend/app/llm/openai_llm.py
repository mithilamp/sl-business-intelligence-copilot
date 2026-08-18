from typing import Type

from openai import OpenAI

from app.core.settings import settings
from pydantic import BaseModel
from app.llm.base import BaseLLM

class OpenAILLM(BaseLLM):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
        )
        return response.choices[0].message.content

    def generate_structured(self, system_prompt: str, user_prompt: str, response_model: Type[BaseModel]) -> BaseModel:
        response = self.client.chat.completions.parse(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            response_format=response_model,
        )
        return response.choices[0].message.parsed