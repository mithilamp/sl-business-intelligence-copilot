"""Crawl and download documents from configured authoritative sources."""

import argparse
import json

import requests

from app.core.logger import logger
from app.core.sources import EXPANSION_SOURCES, SOURCES
from app.ingestion.crawler.static_crawler import StaticCrawler
from app.ingestion.downloader.downloader import Downloader
from app.ingestion.manifest import ManifestDocument, write_manifest
from app.ingestion.metadata.document_classifier import build_document_metadata


def crawl_source(source, max_pages: int, max_pdfs: int, download: bool = True):
    urls = StaticCrawler(source).crawl(max_pages=max_pages, max_pdfs=max_pdfs)
    documents = []
    failures = []
    downloader = Downloader()
    for url in urls:
        if not download:
            continue
        try:
            path = downloader.download(source, url)
        except requests.RequestException as exc:
            failures.append({"document_url": url, "error": str(exc)})
            logger.warning(f"Skipping unavailable document {url}: {exc}")
            continue
        metadata = build_document_metadata(path.name, source)
        documents.append(ManifestDocument(
            filename=path.name, path=str(path.resolve()), document_url=url,
            source=source.name, **metadata,
        ))
    if download:
        write_manifest(source.output_folder / "manifest.json", documents)
        failure_path = source.output_folder / "download_failures.json"
        failure_path.write_text(json.dumps(failures, indent=2), encoding="utf-8")
    logger.info(
        f"{source.name}: discovered {len(urls)}, recorded {len(documents)} documents, "
        f"skipped {len(failures)} unavailable documents"
    )
    return urls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", nargs="*", choices=sorted(SOURCES), default=list(EXPANSION_SOURCES))
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--max-pdfs", type=int, default=30)
    parser.add_argument("--discover-only", action="store_true")
    args = parser.parse_args()
    for key in args.sources:
        crawl_source(SOURCES[key], args.max_pages, args.max_pdfs, not args.discover_only)


if __name__ == "__main__":
    main()
