import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.core.sources import DataSource


@dataclass
class ManifestDocument:
    filename: str
    path: str
    document_url: str
    source: str
    category: str | None = None
    document_type: str | None = None
    published_date: str | None = None
    language: str | None = None
    geography: str | None = None
    sector: str | None = None
    year: int | None = None
    title: str | None = None

    @classmethod
    def from_dict(cls, item: dict[str, Any], source: DataSource) -> "ManifestDocument":
        return cls(
            filename=item["filename"], path=item["path"],
            document_url=item.get("document_url") or item.get("url") or "",
            source=item.get("source", source.name),
            category=item.get("category", source.default_category),
            document_type=item.get("document_type", source.default_document_type),
            published_date=item.get("published_date"),
            language=item.get("language", source.default_language),
            geography=item.get("geography", source.default_geography),
            sector=item.get("sector", source.default_sector),
            year=item.get("year"), title=item.get("title"),
        )


def write_manifest(path: Path, documents: list[ManifestDocument]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(item) for item in documents], indent=2), encoding="utf-8")


def read_manifest(path: Path, source: DataSource) -> list[ManifestDocument]:
    return [ManifestDocument.from_dict(item, source) for item in json.loads(path.read_text(encoding="utf-8"))]
