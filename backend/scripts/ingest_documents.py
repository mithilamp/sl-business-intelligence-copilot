from pathlib import Path
from app.core.sources import CBSL
from app.ingestion.pipeline import IngestionPipeline

pipeline = IngestionPipeline()

pipeline.ingest_pdf(
    source=CBSL,
    pdf_path=Path("../data/raw/central_bank/banks.pdf")
)