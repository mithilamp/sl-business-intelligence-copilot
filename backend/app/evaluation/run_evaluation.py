"""CLI: python -m app.evaluation.run_evaluation [--include-answers]."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from app.evaluation.evaluator import RAGEvaluator
from app.evaluation.metrics import summarise
from app.evaluation.answer_quality import summarise_answer_quality


def _markdown(report: dict) -> str:
    base, current = report["systems"]["vector_only"], report["systems"]["vector_plus_reranker"]
    lines = ["# Retrieval evaluation report", "", f"Generated: {report['generated_at']}", "",
             "## Baseline comparison", "", "| System | Tasks | Hit@3 | MRR | Precision@3 |", "|---|---:|---:|---:|---:|",
             f"| Vector only | {base['total']} | {base['hit_rate_at_3']:.1%} | {base['mean_reciprocal_rank']:.3f} | {base['mean_precision_at_3']:.3f} |",
             f"| Vector + cross-encoder reranker | {current['total']} | {current['hit_rate_at_3']:.1%} | {current['mean_reciprocal_rank']:.3f} | {current['mean_precision_at_3']:.3f} |",
             "", "## Production results by category", "", "| Category | Tasks | Hits | Hit@3 |", "|---|---:|---:|---:|"]
    for category, values in current["category_summary"].items():
        lines.append(f"| {category} | {values['total']} | {values['hits']} | {values['hit_rate_at_3']:.1%} |")
    lines += ["", "## Failure analysis", ""]
    if not current["failures"]:
        lines.append("No expected-source misses were found in the top three results.")
    else:
        for failure in current["failures"]:
            returned = ", ".join(failure["failure"]["returned_authorities"])
            lines.append(f"- **{failure['id']}** ({failure['category']}): expected {', '.join(failure['expected_sources'])}; returned {returned}.")
    lines += ["", "## Interpretation", "",
              "Hit@3 measures whether at least one expected authority appears in the first three unique document results. MRR rewards placing the first relevant authority higher. Precision@3 measures the share of the three returned documents associated with an expected authority.", "",
              "Source matching uses title, filename, publisher, category, document type, date, and URL metadata. Results measure retrieval, not factual answer correctness. Land Intelligence scenarios are maintained separately because they require document fixtures and multimodal execution."]
    quality = report.get("answer_quality", {})
    lines += ["", "## End-to-end answer quality", ""]
    if quality.get("graded_answers"):
        lines += [
            f"- Graded answers: {quality['graded_answers']}",
            f"- Mean groundedness (1–5): {quality['mean_groundedness_1_to_5']:.3f}",
            f"- Mean relevance (1–5): {quality['mean_relevance_1_to_5']:.3f}",
            f"- Mean citation quality (1–5): {quality['mean_citation_quality_1_to_5']:.3f}",
            f"- Answers with unsupported claims: {quality['answers_with_unsupported_claims']}",
            "",
            "These LLM-judge scores require manual spot-checking before presentation.",
        ]
    else:
        lines.append("Not run. Use `--grade-answers` to generate answers and apply the structured groundedness rubric.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-answers", action="store_true", help="Also generate production answers (costs one LLM call per task).")
    parser.add_argument("--grade-answers", action="store_true", help="Generate and grade all answers for groundedness, relevance and citation quality (costs two LLM calls per task).")
    args = parser.parse_args()
    raw = RAGEvaluator().run(
        include_answers=args.include_answers,
        grade_answers=args.grade_answers,
    )
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "benchmark_version": "1.0",
              "systems": {name: summarise(results) for name, results in raw.items()},
              "answer_quality": summarise_answer_quality(raw["vector_plus_reranker"])}
    output_dir = Path(__file__).parent / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evaluation_results.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "evaluation_summary.md").write_text(_markdown(report), encoding="utf-8")
    print(json.dumps({"generated_at": report["generated_at"], "systems": {
        name: {key: value for key, value in values.items() if key not in {"results", "failures"}}
        for name, values in report["systems"].items()}}, indent=2))


if __name__ == "__main__":
    main()
