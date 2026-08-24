from dataclasses import dataclass
from pathlib import Path

from app.core.settings import settings


@dataclass(frozen=True)
class DataSource:
    name: str
    base_url: str
    output_folder: Path
    key: str = ""
    start_urls: tuple[str, ...] = ()
    allowed_domains: tuple[str, ...] = ()
    default_category: str | None = None
    default_document_type: str = "Report"
    default_language: str | None = "English"
    default_geography: str | None = "Sri Lanka"
    default_sector: str | None = None

    @property
    def crawl_start_urls(self) -> tuple[str, ...]:
        return self.start_urls or (self.base_url,)


CBSL = DataSource(
    key="cbsl",
    name="Central Bank of Sri Lanka",
    base_url="https://www.cbsl.gov.lk",
    output_folder=settings.RAW_DATA_DIR / "central_bank",
    default_category="Economy and Finance",
    default_sector="Economy and Finance",
)

BOI = DataSource(
    key="boi", name="Board of Investment of Sri Lanka",
    base_url="https://investsrilanka.com",
    output_folder=settings.RAW_DATA_DIR / "boi",
    start_urls=("https://investsrilanka.com/home/download/",),
    default_category="Investment", default_sector="Investment",
)

DCS = DataSource(
    key="dcs", name="Department of Census and Statistics Sri Lanka",
    base_url="https://www.statistics.gov.lk",
    output_folder=settings.RAW_DATA_DIR / "census_and_statistics",
    start_urls=(
        "https://www.statistics.gov.lk/Publication/newPage",
        "https://www.statistics.gov.lk/LabourForce/StaticalInformation/AnnualReports",
        "https://www.statistics.gov.lk/PublicEmployment/StaticalInformation/CensusReports",
        "https://www.statistics.gov.lk/Publication/Atlas",
    ),
    default_category="Official Statistics",
)

EDB = DataSource(
    key="edb", name="Sri Lanka Export Development Board",
    base_url="https://www.srilankabusiness.com",
    output_folder=settings.RAW_DATA_DIR / "export_development_board",
    start_urls=("https://www.srilankabusiness.com/publications/",),
    default_category="Exports and Trade", default_sector="Exports and Trade",
)

DOA = DataSource(
    key="doa", name="Department of Agriculture Sri Lanka",
    base_url="https://doa.gov.lk",
    output_folder=settings.RAW_DATA_DIR / "agriculture",
    start_urls=(
        "https://doa.gov.lk/doa-publications/",
        "https://doa.gov.lk/sepc-downloads_en/",
        "https://doa.gov.lk/naicc-books/",
        "https://doa.gov.lk/naicc-publications-crop-calender/",
        "https://doa.gov.lk/fcrdi-downloads/",
        "https://doa.gov.lk/rrdi_downloads-2/",
        "https://doa.gov.lk/spmdc-downloads_en/",
        "https://doa.gov.lk/download-doa/",
    ),
    default_category="Agriculture", default_sector="Agriculture",
)

SOURCES = {source.key: source for source in (CBSL, BOI, DCS, EDB, DOA)}
EXPANSION_SOURCES = {source.key: source for source in (BOI, DCS, EDB, DOA)}
