import hashlib
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.core.sources import DataSource
from requests import Session

from app.core.logger import logger


class Downloader:
    def __init__(self,session: Session | None = None):
        self.session = session or requests.Session()
        if session is None:
            retries = Retry(
                total=2,
                connect=2,
                read=2,
                status=2,
                backoff_factor=0.5,
                status_forcelist=(429, 500, 502, 503, 504),
                allowed_methods=("GET",),
            )
            self.session.mount("http://", HTTPAdapter(max_retries=retries))
            self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def download(self, source: DataSource, url: str) -> Path:

        output_dir = Path(source.output_folder)
        output_dir.mkdir(parents=True, exist_ok=True)

        parsed_url = urlparse(url)
        filename = unquote(Path(parsed_url.path).name)
        if parsed_url.netloc == "drive.usercontent.google.com":
            drive_id = parse_qs(parsed_url.query).get("id", [None])[0]
            filename = f"google-drive-{drive_id or hashlib.sha256(url.encode()).hexdigest()[:12]}.pdf"
        elif not filename:
            filename = f"document-{hashlib.sha256(url.encode()).hexdigest()[:12]}.pdf"
        if not filename.lower().endswith(".pdf"):
            filename = f"{filename}.pdf"
        destination = output_dir / filename

        if destination.exists():
            logger.info(f"{filename} already exists. Skipping.")
            return destination

        logger.info(f"Downloading {filename}")
        
        response = self.session.get(
            url,
            timeout=60,
            headers={"User-Agent": "Mozilla/5.0 (compatible; SLBusinessIntelligenceCopilot/1.0)"},
        )
        response.raise_for_status()

        destination.write_bytes(response.content)
        logger.info(f"Downloaded {filename}")

        return destination
