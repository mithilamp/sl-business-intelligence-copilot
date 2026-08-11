from app.core.logger import logger
from app.core.sources import CBSL
from app.ingestion.crawler.static_crawler import StaticCrawler
from app.ingestion.downloader.downloader import Downloader

crawler = StaticCrawler(CBSL)
downloader = Downloader()

logger.info("Fetching homepage...")

html = crawler.fetch()

logger.info("Extracting links...")

links = crawler.get_links(html)

logger.info(f"Found {len(links)} links.")

logger.info("Searching for PDF links...")

pdf_links = crawler.get_pdf_links(links)

for pdf in pdf_links[:10]:
    print(pdf)

logger.info(f"Found {len(pdf_links)} PDF links.")

for pdf_url in pdf_links[:3]:

    downloader.download(
        CBSL,
        pdf_url,
    )