from fileinput import filename
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests

from app.core.sources import DataSource
from requests import Session

from app.core.logger import logger


class Downloader:
    def __init__(self,session: Session | None = None):
        self.session = session or requests.Session()

    def download(self, source: DataSource, url: str) -> Path:

        output_dir = Path(source.output_folder)
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = unquote(Path(urlparse(url).path).name)
        destination = output_dir / filename

        if destination.exists():
            logger.info(f"{filename} already exists. Skipping.")
            return destination

        logger.info(f"Downloading {filename}")
        
        response = self.session.get(url, timeout=60)
        response.raise_for_status()

        destination.write_bytes(response.content)
        logger.info(f"Downloaded {filename}")

        return destination