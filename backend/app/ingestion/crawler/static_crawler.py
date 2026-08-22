import requests

from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from app.core.sources import DataSource
from app.ingestion.crawler.base import BaseCrawler
from app.core.logger import logger


class StaticCrawler(BaseCrawler):

    def __init__(
        self,
        source: DataSource,
        session: Session | None = None,
    ):
        self.source = source
        self.session = session or requests.Session()

    def fetch(self, url: str | None = None) -> str:

        target_url = url or self.source.base_url

        logger.info(f"Fetching {target_url}")

        response = self.session.get(
            target_url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        response.raise_for_status()

        return response.text

    def get_links(self, html: str, base_url: str | None = None):

        page_url = base_url or self.source.base_url

        soup = BeautifulSoup(html, "html.parser")

        links = set()

        for tag in soup.find_all("a", href=True):

            href = tag["href"].strip()

            if not href:
                continue

            if href.startswith("#"):
                continue

            if href.startswith("javascript:"):
                continue

            href = urljoin(page_url, href)

            links.add(href)

        logger.info(
            f"Discovered {len(links)} links from {page_url}"
        )

        return sorted(links)

    def get_pdf_links(self, links: list[str]):

        pdf_links = {
            link
            for link in links
            if urlparse(link).path.lower().endswith(".pdf")
        }

        logger.info(
            f"Discovered {len(pdf_links)} PDF links."
        )

        return sorted(pdf_links)

    def is_internal_link(self, url: str) -> bool:

        source_domain = urlparse(
            self.source.base_url
        ).netloc

        link_domain = urlparse(url).netloc

        return (
            link_domain == source_domain
            or link_domain.endswith(
                "." + source_domain
            )
        )

    def crawl(
        self,
        max_pages: int = 20,
        max_pdfs: int = 30,
    ) -> list[str]:

        pages_to_visit = [self.source.base_url]

        visited_pages = set()
        discovered_pdfs = set()

        while (
            pages_to_visit
            and len(visited_pages) < max_pages
            and len(discovered_pdfs) < max_pdfs
        ):

            current_url = pages_to_visit.pop(0)

            if current_url in visited_pages:
                continue

            if not self.is_internal_link(current_url):
                continue

            visited_pages.add(current_url)

            try:

                html = self.fetch(current_url)

                links = self.get_links(
                    html,
                    base_url=current_url,
                )

                pdf_links = self.get_pdf_links(links)

                discovered_pdfs.update(pdf_links)

                logger.info(
                    f"Visited {len(visited_pages)}/{max_pages} pages"
                )

                for link in links:

                    if (
                        link not in visited_pages
                        and self.is_internal_link(link)
                    ):
                        pages_to_visit.append(link)

            except requests.RequestException as exc:

                logger.warning(
                    f"Failed to crawl {current_url}: {exc}"
                )

        pdfs = sorted(discovered_pdfs)

        logger.info(
            f"Crawl complete. "
            f"Pages: {len(visited_pages)}, "
            f"PDFs: {len(pdfs)}"
        )

        return pdfs[:max_pdfs]