import re


def classify_document(filename: str):

    name = filename.lower()

    category = "General"
    document_type = "Report"


    # -------------------------
    # Category classification
    # -------------------------

    if "fssr" in name:
        category = "Financial Stability"

    elif "financial" in name or "stability" in name:
        category = "Financial Stability"

    elif "bank" in name:
        category = "Banking"

    elif "pmi" in name:
        category = "Business Activity"

    elif "policy" in name:
        category = "Economic Policy"

    elif "market" in name or "omo" in name:
        category = "Financial Markets"


    # -------------------------
    # Document type
    # -------------------------

    if "speech" in name:
        document_type = "Speech"

    elif "notice" in name:
        document_type = "Notice"

    elif "presentation" in name:
        document_type = "Presentation"

    elif "report" in name or "fssr" in name:
        document_type = "Report"


    return {
        "category": category,
        "document_type": document_type,
        "year": extract_year(filename),
    }


def extract_year(value: str) -> int | None:
    years = re.findall(r"(?<!\d)(?:19|20)\d{2}(?!\d)", value)
    return int(years[-1]) if years else None


def build_document_metadata(filename: str, source) -> dict:
    """Combine conservative filename inference with publisher defaults."""
    inferred = classify_document(filename)
    name = filename.lower()
    document_type = inferred["document_type"]
    if "annual" in name:
        document_type = "Annual Report"
    elif "bulletin" in name:
        document_type = "Bulletin"
    elif "guide" in name or "guideline" in name:
        document_type = "Guide"
    elif "survey" in name or "census" in name:
        document_type = "Statistical Report"
    elif "research" in name or "journal" in name:
        document_type = "Research Paper"

    published_year = inferred["year"]
    return {
        "category": source.default_category or inferred["category"],
        "document_type": document_type or source.default_document_type,
        "published_date": str(published_year) if published_year else None,
        "language": source.default_language,
        "geography": source.default_geography,
        "sector": source.default_sector,
        "year": published_year,
    }
