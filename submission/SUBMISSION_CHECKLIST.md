# Submission audit

Audit date: 5 September 2026. Report and evidence describe application source at commit `adbebd6f03c8d6fb96bb1db1a3805fa5f962899a` on `fine-tune`. Submission documents are added in a subsequent commit. Application functionality was not modified during preparation.

## Deliverables and remaining checks

| Requirement | Status |
|---|---|
| Source and professional README | Source, architecture diagram, setup, technology list and demo instructions are in this repository. |
| RAG and citations | Implemented with PostgreSQL/pgvector, reranking and answer source metadata. |
| Agent decisions and memory | /agent chooses between Knowledge Search and Business Advisor and records a routing reason; conversations persist in PostgreSQL. |
| Real trace evidence | Agent screenshot included. Land instrumentation exists, but a separate land-run screenshot/link was not found among available submission assets. |
| Multimodal component | Vision interprets land-plan images/PDFs and combines them with geographic evidence. |
| Evaluation and baseline | Thirty retrieval tasks, recorded metrics, vector-only comparison and failure analysis included. Six land scenarios are definitions, not executed benchmark results. |
| Deployment | Local browser deployment is acceptable. A public application URL is a bonus. |
| Presentation | Delivered successfully according to the presenter; 16-slide deck included with clarifications. |
| Written report | Four-page PDF and DOCX included. Original brief's three-page maximum annotation requires confirmation. |

## Validation results

- Frontend ESLint passed.
- A production build with `next build --webpack` passed in a copy of the source using existing dependencies. TypeScript checking and static generation passed. A clean dependency install and default Turbopack build were not tested.
- Five deterministic evaluation-metric tests passed via direct invocation. This was not a pytest-suite run.
- The full backend pytest attempt could not start: the available local virtual environment lacks pytest despite its presence in requirements.txt. That environment is Python 3.9; README calls for Python 3.11+. Use a supported environment and install the listed dependencies before rerunning the suite.
- Evaluation results were retained from 27 August 2026. No fresh model/database end-to-end evaluation was performed during the audit.
- The report was rendered and visually checked at exactly four pages.
- Real environment files, dependencies, build outputs and uploaded documents are excluded from submission materials.

## Reproduction notes

A clean setup needs PostgreSQL with the vector extension and a document corpus. Ingestion expects manifests. After environment and database setup, run from backend:

```bash
../.venv/bin/python -m scripts.crawl_sources cbsl boi dcs edb doa --max-pages 20 --max-pdfs 30
../.venv/bin/python -m scripts.ingest_sources cbsl boi dcs edb doa
../.venv/bin/python -m pytest tests -q
../.venv/bin/python -m app.evaluation.run_evaluation
```

Crawling and evaluation require network access; embedding and generation incur provider usage. Current crawling may retrieve a different corpus from the August benchmark. Exact reproduction also requires the original corpus and model configuration. Some legacy tests perform network calls during import.

## Before final handoff

1. Confirm whether the four-page report is accepted despite the brief's three-page annotation.
2. Share the `fine-tune` branch or the submission commit, so the assessor sees these files rather than an older default branch.
3. Verify that the branch URL opens while signed out. Remote accessibility through Git credentials does not establish public visibility.
4. Add any separate land-trace screenshot/link used in the presentation if available. An actual general agent trace is already included.
5. Enter the required author/student details in the submission portal or report. No personal details were invented.

See [presentation clarifications](PRESENTATION_CORRECTIONS.md) for deployment, metric and routing corrections. Human-reviewed answer grading, executed land tests and a comparison with equal document-selection budgets remain future evaluation work.
