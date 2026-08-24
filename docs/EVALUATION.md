# Evaluation methodology

## Coverage

`benchmark_questions.json` contains 30 RAG questions across economy, investment, agriculture, exports, official statistics, tourism, tax/compliance, and cross-domain reasoning. `land_intelligence_tasks.json` adds six equivalent multimodal tasks covering extraction, multi-page processing, missing locations, broad geocode fallbacks, nearby infrastructure, and tourism analysis.

## Controlled baseline

Both systems receive the same query and initial 20 vector candidates:

- Baseline: return the first three vector-similarity candidates.
- Production: cross-encoder rerank all 20 and return the best three.

This isolates the reranker's effect. It does not compare answer-generation models.

## Metrics

- Hit@3: at least one expected authority appears in the first three results.
- Mean reciprocal rank (MRR): rewards a relevant authority at a higher rank.
- Precision@3: fraction of the first three documents associated with an expected authority.
- Category Hit@3: exposes weak domains that an aggregate score could hide.
- Failure record: stores expected sources and returned publishers for every miss.

Matching is case-insensitive and metadata-aware across title, filename, publisher, category, document type, publication date, and URL. Pipe-separated aliases support common names such as `CBSL|Central Bank of Sri Lanka`.

## Running and reporting

From `backend/`, run `python -m app.evaluation.run_evaluation`. The JSON output is machine-readable; the Markdown summary is ready for a slide appendix. Use `--include-answers` only for qualitative review because it adds cost and variability.

Do not present an old report as a current result after the corpus changes. Regenerate it and record the date, corpus/version, model names, and environment alongside presentation metrics.

## End-to-end answer quality

Run `python -m app.evaluation.run_evaluation --grade-answers` for the final quality evaluation. It generates each production answer and applies a structured 1–5 rubric for groundedness, relevance, and citation quality, while recording unsupported claims and a short failure analysis.

The verified 30-answer run produced mean scores of 4.533 groundedness, 4.667 relevance, and 4.667 citation quality. Thirteen answers contained at least one flagged unsupported claim. These are LLM-judge measurements and require manual spot-checking; they do not replace expert factual review.

This path costs two model calls per task and should be run intentionally. Treat LLM judging as evidence that requires manual spot-checking, not as ground truth. The report states `not_run` until the live grading command completes; no score should be presented before that run.

## Land-task execution

The land suite is a task specification because representative land documents require permission and cannot safely be committed by default. For final evaluation, select consented fixtures for a clear image, multi-page PDF, missing-location case, and broad-location case. Record field completeness, invalid-JSON rate, geocode outcome, nearby-data completeness, report uncertainty, latency, and whether all expected LangSmith spans appear.

## Limitations

Expected-source retrieval is a proxy for relevance. It does not prove that every claim is factually correct, complete, or entailed by the retrieved text. The documented judge rubric provides repeatable end-to-end evidence, but expert/manual review is still required before treating those scores as factual correctness.
