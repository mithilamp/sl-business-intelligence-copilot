from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

class Settings(BaseSettings):
    PROJECT_NAME: str = "SL Business Intelligence Copilot"
    DATA_DIR: Path = DATA_DIR
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    EMBEDDINGS_DIR: Path = DATA_DIR / "embeddings"
    CHUNK_DIR: Path = DATA_DIR / "chunks"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"
    DATABASE_URL: str 
    OPENAI_API_KEY: str

    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_TRACING: bool = False
    LANGSMITH_PROJECT: str = "sl-business-intelligence-copilot"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
