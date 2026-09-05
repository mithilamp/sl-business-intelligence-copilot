from pathlib import Path

import json
import requests

from app.core.sources import BOI, DCS, DOA, EDB, EXPANSION_SOURCES, DataSource
from app.ingestion.manifest import ManifestDocument, read_manifest, write_manifest
from app.ingestion.metadata.document_classifier import build_document_metadata
from app.ingestion.crawler.static_crawler import StaticCrawler
from scripts.crawl_sources import crawl_source


def test_expansion_sources_have_publication_seeds_and_metadata_defaults():
    assert set(EXPANSION_SOURCES) == {"boi", "dcs", "edb", "doa"}
    for source in (BOI, DCS, EDB, DOA):
        assert source.crawl_start_urls
        assert source.default_category
        assert source.default_geography == "Sri Lanka"


def test_manifest_round_trip_preserves_source_metadata(tmp_path: Path):
    path = tmp_path / "manifest.json"
    item = ManifestDocument(
        filename="annual-report-2024.pdf", path="/tmp/annual-report-2024.pdf",
        document_url="https://example.test/annual-report-2024.pdf", source=BOI.name,
        category="Investment", document_type="Annual Report", published_date="2024",
        language="English", geography="Sri Lanka", sector="Investment", year=2024,
    )
    write_manifest(path, [item])
    assert read_manifest(path, BOI) == [item]


def test_metadata_inference_uses_source_defaults_and_year():
    metadata = build_document_metadata("BOI-Annual-Report-2023.pdf", BOI)
    assert metadata["category"] == "Investment"
    assert metadata["document_type"] == "Annual Report"
    assert metadata["year"] == 2023
    assert metadata["published_date"] == "2023"


def test_static_crawler_uses_all_configured_seed_pages(monkeypatch):
    crawler = StaticCrawler(DOA)
    fetched = []

    def fake_fetch(url):
        fetched.append(url)
        return '<a href="/files/agriculture-report-2024.pdf">Report</a>'

    monkeypatch.setattr(crawler, "fetch", fake_fetch)
    assert crawler.crawl(max_pages=len(DOA.start_urls), max_pdfs=5) == [
        "https://doa.gov.lk/files/agriculture-report-2024.pdf"
    ]
    assert fetched == list(DOA.start_urls)


def test_source_download_continues_after_unavailable_document(monkeypatch, tmp_path: Path):
    source = DataSource("Test", "https://example.test", tmp_path, key="test")
    urls = ["https://example.test/broken.pdf", "https://example.test/good.pdf"]
    good_path = tmp_path / "good.pdf"
    good_path.write_bytes(b"%PDF")

    monkeypatch.setattr(StaticCrawler, "crawl", lambda *_args, **_kwargs: urls)

    def fake_download(_self, _source, url):
        if url.endswith("broken.pdf"):
            raise requests.ConnectionError("remote closed connection")
        return good_path

    monkeypatch.setattr("scripts.crawl_sources.Downloader.download", fake_download)
    assert crawl_source(source, 2, 2) == urls
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    failures = json.loads((tmp_path / "download_failures.json").read_text())
    assert [item["filename"] for item in manifest] == ["good.pdf"]
    assert failures[0]["document_url"].endswith("broken.pdf")


def test_doa_discovers_embedded_google_drive_publications():
    crawler = StaticCrawler(DOA)
    html = """[vc_btn title=“E” link=“url:https://drive.google.com/file/d/abc123/view?usp=sharing|target:_blank”]"""
    links = crawler.get_links(html, DOA.base_url)
    assert crawler.get_pdf_links(links) == [
        "https://drive.usercontent.google.com/download?id=abc123&export=download&confirm=t"
    ]
