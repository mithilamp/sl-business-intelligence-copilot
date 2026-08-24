# Retrieval evaluation report

Generated: 2026-08-24T18:39:35.237305+00:00

## Baseline comparison

| System | Tasks | Hit@3 | MRR | Precision@3 |
|---|---:|---:|---:|---:|
| Vector only | 30 | 70.0% | 0.611 | 0.556 |
| Vector + cross-encoder reranker | 30 | 66.7% | 0.600 | 0.400 |

## Production results by category

| Category | Tasks | Hits | Hit@3 |
|---|---:|---:|---:|
| agriculture | 5 | 4 | 80.0% |
| cross_domain | 1 | 1 | 100.0% |
| economy | 5 | 3 | 60.0% |
| export | 5 | 4 | 80.0% |
| investment | 5 | 5 | 100.0% |
| statistics | 5 | 1 | 20.0% |
| tax_and_compliance | 1 | 0 | 0.0% |
| tourism | 3 | 2 | 66.7% |

## Failure analysis

- **economy_001** (economy): expected Central Bank of Sri Lanka|CBSL; returned Board of Investment of Sri Lanka, Sri Lanka Export Development Board.
- **economy_005** (economy): expected International Monetary Fund|IMF; returned Central Bank of Sri Lanka.
- **agriculture_001** (agriculture): expected Department of Agriculture; returned Sri Lanka Export Development Board.
- **export_004** (export): expected Sri Lanka Customs|Customs; returned Board of Investment of Sri Lanka, Sri Lanka Export Development Board.
- **statistics_001** (statistics): expected Department of Census and Statistics|DCS; returned Central Bank of Sri Lanka, Department of Agriculture Sri Lanka.
- **statistics_002** (statistics): expected Department of Census and Statistics|DCS; returned Central Bank of Sri Lanka.
- **statistics_003** (statistics): expected Department of Census and Statistics|DCS; returned Board of Investment of Sri Lanka, Central Bank of Sri Lanka, Department of Agriculture Sri Lanka.
- **statistics_004** (statistics): expected Department of Census and Statistics|DCS; returned Central Bank of Sri Lanka, Department of Agriculture Sri Lanka.
- **tourism_003** (tourism): expected Central Bank of Sri Lanka|CBSL; returned Board of Investment of Sri Lanka.
- **tax_001** (tax_and_compliance): expected Inland Revenue Department|IRD; returned Board of Investment of Sri Lanka, Central Bank of Sri Lanka.

## Interpretation

Hit@3 measures whether at least one expected authority appears in the first three unique document results. MRR rewards placing the first relevant authority higher. Precision@3 measures the share of the three returned documents associated with an expected authority.

Source matching uses title, filename, publisher, category, document type, date, and URL metadata. Results measure retrieval, not factual answer correctness. Land Intelligence scenarios are maintained separately because they require document fixtures and multimodal execution.

## End-to-end answer quality

- Graded answers: 30
- Mean groundedness (1–5): 4.533
- Mean relevance (1–5): 4.667
- Mean citation quality (1–5): 4.667
- Answers with unsupported claims: 13

These LLM-judge scores require manual spot-checking before presentation.
