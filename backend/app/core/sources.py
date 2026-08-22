from dataclasses import dataclass
from pathlib import Path
from app.core.settings import settings


@dataclass
class DataSource:
    name: str
    base_url: str
    output_folder: str
    default_category: str | None = None
    default_language: str | None = "English"


CBSL = DataSource(
    name="Central Bank of Sri Lanka",
    base_url="https://www.cbsl.gov.lk",
    output_folder=settings.RAW_DATA_DIR / "central_bank",
    default_category="Economy and Finance",
)