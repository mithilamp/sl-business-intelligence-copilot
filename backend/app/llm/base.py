from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        pass

    @abstractmethod
    def generate_structured(self, system_prompt: str, user_prompt: str, response_model: Type[BaseModel]) -> BaseModel:
        pass