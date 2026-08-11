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

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()