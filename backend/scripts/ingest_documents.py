import json
from pathlib import Path

from app.core.sources import CBSL
from app.ingestion.pipeline import IngestionPipeline
from app.core.settings import settings

pipeline = IngestionPipeline()


manifest = (
    settings.RAW_DATA_DIR/ "central_bank"/ "manifest.json"
)


documents = json.loads(
    manifest.read_text(
        encoding="utf-8"
    )
)


for item in documents:

    pdf_path = Path(item["path"])

    print(f"Ingesting {pdf_path.name}")

    pipeline.ingest_pdf(
        source=CBSL,
        pdf_path=pdf_path,
        document_url=item["url"],
    )