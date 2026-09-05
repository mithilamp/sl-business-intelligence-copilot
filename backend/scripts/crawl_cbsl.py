from app.core.logger import logger
from app.core.sources import CBSL
from app.ingestion.crawler.static_crawler import StaticCrawler
from app.ingestion.downloader.downloader import Downloader
import json

crawler = StaticCrawler(CBSL)
downloader = Downloader()


logger.info("Starting CBSL crawl...")


pdf_links = crawler.crawl(
    max_pages=20,
    max_pdfs=30,
)


logger.info(
    f"Found {len(pdf_links)} PDF links."
)


for pdf in pdf_links:
    print(pdf)


logger.info("Downloading PDFs...")

documents = []

for pdf_url in pdf_links[:30]:

    pdf_path = downloader.download(
        CBSL,
        pdf_url,
    )

    documents.append(
        {
            "filename": pdf_path.name,
            "path": str(pdf_path.resolve()),
            "url": pdf_url,
        }
    )


manifest_path = CBSL.output_folder / "manifest.json"


manifest_path.write_text(
    json.dumps(
        documents,
        indent=2,
    ),
    encoding="utf-8",
)


logger.info(
    f"Created manifest file: {manifest_path}"
)


logger.info("CBSL crawl finished.")