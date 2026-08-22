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
    }