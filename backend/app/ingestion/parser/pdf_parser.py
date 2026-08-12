import pymupdf
from pathlib import Path

from app.core.logger import logger
from app.ingestion.parser.base import BaseParser

class PDFParser(BaseParser):

    def parse(self, pdf_path: Path) -> str:
        logger.info(f"Parsing {pdf_path.name}")

        with pymupdf.open(pdf_path) as document:
            pages = []

            for page in document:
                page_text = page.get_text().strip()

                if page_text:
                    pages.append(page_text)

        text = "\n".join(pages)

        logger.info(f"Extracted text from {pdf_path.name}")

        return text