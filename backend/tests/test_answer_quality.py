from app.evaluation.answer_quality import summarise_answer_quality


def test_answer_quality_summary_reports_means_and_unsupported_claims():
    results = [
        {"answer_quality": {"groundedness": 5, "relevance": 4, "citation_quality": 3,
                            "unsupported_claims": [], "failure_analysis": "None"}},
        {"answer_quality": {"groundedness": 3, "relevance": 5, "citation_quality": 4,
                            "unsupported_claims": ["Unsupported number"], "failure_analysis": "One claim"}},
    ]

    summary = summarise_answer_quality(results)

    assert summary["graded_answers"] == 2
    assert summary["mean_groundedness_1_to_5"] == 4
    assert summary["mean_relevance_1_to_5"] == 4.5
    assert summary["answers_with_unsupported_claims"] == 1


def test_answer_quality_summary_is_explicit_when_not_run():
    assert summarise_answer_quality([]) == {"graded_answers": 0, "status": "not_run"}
