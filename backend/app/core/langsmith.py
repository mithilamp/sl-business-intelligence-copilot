import os

from app.core.settings import settings
from langsmith import traceable


os.environ["LANGSMITH_TRACING"] = str(
    settings.LANGSMITH_TRACING
).lower()

os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT

if settings.LANGSMITH_API_KEY:
    os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY

if settings.LANGSMITH_ENDPOINT:
    os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT


__all__ = ["traceable"]