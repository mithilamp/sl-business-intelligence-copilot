from app.evaluation.metrics import precision_at_k, reciprocal_rank, source_hit, summarise


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


def test_aliases_and_rank_aware_metrics():
    retrieved_sources = [
        {"source": "Unrelated Publisher"},
        {"source": "Central Bank of Sri Lanka"},
        {"source": "Central Bank of Sri Lanka"},
    ]
    expected = ["CBSL|Central Bank of Sri Lanka"]
    assert source_hit(expected, retrieved_sources)
    assert reciprocal_rank(expected, retrieved_sources) == 0.5
    assert precision_at_k(expected, retrieved_sources, 3) == 0.6667


def test_summary_records_category_and_failure_details():
    report = summarise([
        {"id": "ok", "question": "q", "category": "economy", "expected_sources": ["CBSL"],
         "retrieved_sources": [{"source": "CBSL"}]},
        {"id": "miss", "question": "q2", "category": "economy", "expected_sources": ["BOI"],
         "retrieved_sources": [{"source": "CBSL"}]},
    ])
    assert report["hit_rate_at_3"] == 0.5
    assert report["category_summary"]["economy"]["hits"] == 1
    assert report["failures"][0]["id"] == "miss"
