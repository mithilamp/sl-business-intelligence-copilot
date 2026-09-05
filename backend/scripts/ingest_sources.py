"""Ingest one or more source manifests into the existing vector store."""

import argparse
from pathlib import Path

from app.core.sources import SOURCES
from app.ingestion.manifest import read_manifest
from app.ingestion.pipeline import IngestionPipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", nargs="+", choices=sorted(SOURCES))
    args = parser.parse_args()
    pipeline = IngestionPipeline()
    for key in args.sources:
        source = SOURCES[key]
        for item in read_manifest(source.output_folder / "manifest.json", source):
            metadata = {
                "title": item.title, "category": item.category,
                "document_type": item.document_type, "published_date": item.published_date,
                "language": item.language, "geography": item.geography,
                "sector": item.sector, "year": item.year,
            }
            pipeline.ingest_pdf(source, Path(item.path), item.document_url, metadata)


if __name__ == "__main__":
    main()
