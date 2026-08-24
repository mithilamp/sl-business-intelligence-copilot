from app.evaluation.metrics import source_hit


def test_source_hit_matches_source_metadata():
    retrieved_sources = [
        {
            "title": "Annual Report 2020",
            "filename": "Annual-Report-2020.pdf",
            "source": "Board of Investment of Sri Lanka",
            "category": "investment",
            "document_type": "annual_report",
            "published_date": "2020",
            "document_url": "https://example.test/annual-report",
        }
    ]

    assert source_hit(["Board of Investment"], retrieved_sources)


def test_source_hit_matches_other_metadata_fields():
    retrieved_sources = [
        {
            "title": "Agriculture Business Guide",
            "filename": "guide.pdf",
            "source": None,
            "category": "Department of Agriculture",
            "document_type": "guide",
            "published_date": None,
            "document_url": None,
        }
    ]

    assert source_hit(["Department of Agriculture"], retrieved_sources)


def test_source_hit_returns_false_when_metadata_does_not_match():
    retrieved_sources = [
        {
            "title": "Business Guide",
            "filename": "guide.pdf",
            "source": "Sampath Bank",
            "category": "finance",
            "document_type": "guide",
            "published_date": None,
            "document_url": None,
        }
    ]

    assert not source_hit(["Central Bank of Sri Lanka"], retrieved_sources)
