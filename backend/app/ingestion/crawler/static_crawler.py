from os import link
import requests
from requests import Session
from app.core.sources import DataSource
from app.ingestion.crawler.base import BaseCrawler
from app.core.logger import logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse


class StaticCrawler(BaseCrawler):

    def __init__(
        self,
        source: DataSource,
        session: Session | None = None,
    ):
        self.source = source
        self.session = session or requests.Session()

    def fetch(self):

        logger.info(f"Fetching {self.source.base_url}")

        response = self.session.get(
            self.source.base_url,
            timeout=30,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        return response.text

    def get_links(self, html: str):

        soup = BeautifulSoup(html, "html.parser")

        links = set()

        for tag in soup.find_all("a", href=True):

            href = tag["href"]

            if href.startswith("#"):
                continue

            if href.startswith("javascript:"):
                continue

            href = urljoin(
                self.source.base_url,
                href
            )

            links.add(href)

        logger.info(f"Discovered {len(links)} links.")

        return sorted(links)

    def get_pdf_links(self, links: list[str]):

        pdf_links = {
            link
            for link in links
            if urlparse(link).path.lower().endswith(".pdf")
        }

        logger.info(f"Discovered {len(pdf_links)} PDF links.")

        return sorted(pdf_links)