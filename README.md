# Sri Lanka Business Intelligence Copilot

An evidence-led AI copilot for researching Sri Lankan business conditions and assessing business opportunities for land. The application combines retrieval-augmented generation (RAG), agentic tool selection, conversational memory, multimodal land-document analysis, geospatial enrichment, evaluation, and LangSmith observability in a responsive web interface.

## What the application does

- **Ask AI:** answers questions about Sri Lankan investment, exports, agriculture, statistics, tourism, and economic conditions using retrieved documents and visible source information.
- **Business Advisor:** turns retrieved evidence—or a generated land report—into recommendations, risks, and verification steps.
- **Land Intelligence:** accepts PDF, PNG, JPG, or JPEG land documents; extracts evidence with vision; normalizes and geocodes the location; retrieves nearby OpenStreetMap information; and produces a structured business assessment.
- **Conversation history:** stores conversations and contextualizes follow-up questions.
- **Observability:** records multi-step Agent and Land Intelligence runs in LangSmith.

## Architecture

```mermaid
flowchart LR
    U[User] --> UI[Next.js interface]
    UI --> API[FastAPI API]

    API --> AR[Business Copilot Agent]
    AR --> MEM[Conversation memory]
    AR --> ROUTE{Tool selection}
    ROUTE --> RAG[Knowledge Search]
    ROUTE --> BA[Business Advisor]

    RAG --> VEC[pgvector retrieval]
    VEC --> RR[Cross-encoder reranker]
    RR --> LLM[Grounded answer]
    LLM --> SRC[Citations and source metadata]

    API --> LA[Land Intelligence Agent]
    LA --> PARSE[Document parser]
    PARSE --> VISION[Vision extraction]
    VISION --> LOC[Location normalization]
    LOC --> OSM[OpenStreetMap geolocation and nearby places]
    OSM --> REPORT[Land business report]
    REPORT --> BA

    AR -. traces .-> LS[LangSmith]
    LA -. traces .-> LS
```

## Main components

| Component | Implementation |
|---|---|
| Web interface | Next.js 16, React 19, TypeScript and Tailwind CSS |
| API | FastAPI |
| Database and vector search | PostgreSQL and pgvector |
| Embeddings | OpenAI `text-embedding-3-small` |
| Reranking | `cross-encoder/ms-marco-MiniLM-L-12-v2` |
| Agent routing | Structured LLM decision between Knowledge Search and Business Advisor |
| Memory | PostgreSQL conversations and messages with follow-up contextualization |
| Land analysis | PDF/image parsing, vision extraction and structured reporting |
| Geospatial enrichment | OpenStreetMap Nominatim and Overpass API |
| Observability | LangSmith traces for agent, RAG and land-analysis stages |

## Data sources

The repository's ingestion configuration includes official documents from:

- Central Bank of Sri Lanka
- Board of Investment of Sri Lanka
- Department of Census and Statistics Sri Lanka
- Sri Lanka Export Development Board
- Department of Agriculture Sri Lanka

Land Intelligence additionally uses user-provided land documents and OpenStreetMap data. The generated report separates document evidence, external geospatial evidence, and AI inferences.

## Repository structure

```text
backend/
  app/agents/        Agent router and land agent
  app/evaluation/    Benchmark datasets, metrics and reports
  app/ingestion/     Crawling, parsing, chunking and ingestion
  app/land/          Multimodal and geospatial land workflow
  app/rag/           Retrieval, reranking and grounded generation
  tests/             Backend test suite
frontend/
  app/               Next.js application
  components/        Ask AI, source, advisor and land UI components
  services/          Backend API client
```

## Local setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL with the pgvector extension
- An OpenAI API key
- A LangSmith API key if tracing is enabled

### Backend

Create `backend/.env` without committing it:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
OPENAI_API_KEY=your_openai_key

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=sl-business-intelligence-copilot
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
CORS_ORIGINS=http://localhost:3000
```

Install dependencies and initialize the tables:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

cd backend
../.venv/bin/python -m scripts.create_tables
```

The application requires an existing ingested document collection. Source manifests can be ingested with:

```bash
../.venv/bin/python -m scripts.ingest_sources cbsl boi dcs edb doa
```

Start the API:

```bash
../.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

API documentation is available at `http://localhost:8000/docs`.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## API workflows

| Endpoint | Purpose |
|---|---|
| `POST /agent` | Agent-routed question answering or business advice |
| `POST /ask` | Direct RAG question answering |
| `POST /business-advice` | Evidence-led business recommendations |
| `POST /land-analysis` | PDF/image land analysis |
| `GET /conversations` | Conversation history |
| `GET /conversations/{id}` | Restore a conversation and its messages |

## Evaluation

The retrieval benchmark contains 30 questions spanning agriculture, economy, exports, investment, statistics, tax/compliance, tourism, and cross-domain queries. Expected-source matching uses document title, filename, publisher, category, document type, date, and URL metadata.

Run the reproducible baseline comparison:

```bash
cd backend
../.venv/bin/python -m app.evaluation.run_evaluation
```

Optional end-to-end answer grading uses additional model calls:

```bash
../.venv/bin/python -m app.evaluation.run_evaluation --grade-answers
```

The generated files are:

- `backend/app/evaluation/reports/evaluation_summary.md`
- `backend/app/evaluation/reports/evaluation_results.json`

### Current retrieval results

| System | Tasks | Hit@3 | MRR | Precision@3 |
|---|---:|---:|---:|---:|
| Vector only | 30 | 70.0% | 0.611 | 0.556 |
| Vector + cross-encoder reranker | 30 | 66.7% | 0.600 | 0.400 |

Investment achieved 100% Hit@3; agriculture and exports achieved 80%. Statistics and tax/compliance produced the largest source-retrieval gaps. On this benchmark, the reranked pipeline did not outperform the vector-only baseline, indicating a need for domain-specific reranker tuning and stronger source coverage. These results measure retrieval and source selection, not end-to-end factual correctness.

Six additional scenarios in `backend/app/evaluation/datasets/land_intelligence_tasks.json` define multimodal Land Intelligence coverage.

## Tracing and observability

With LangSmith enabled, a general Agent run records:

```text
Business Copilot Agent
├── Question Contextualizer
├── Choose Agent Tool
└── RAG Pipeline or Business Advisor
    ├── Retrieve Documents
    ├── Reranker
    └── LLM Generation
```

A complete Land Intelligence run records:

```text
Land Intelligence Analysis
├── Parse Land Document
├── Vision Evidence Extraction
├── Normalize Location
├── Geolocate and Enrich
│   └── Nearby OpenStreetMap Intelligence
├── Land Business Analysis
└── Build Land Intelligence Report
```

For presentation evidence, show the expanded trace tree and the root input/output. Do not expose API keys or sensitive document content.

## Validation

Run the backend tests:

```bash
cd backend
../.venv/bin/python -m pytest -q
```

Run the frontend checks:

```bash
cd frontend
npm run lint
npm run build
```

## Demo flow

1. Ask: **Which sectors are promoted for foreign investment in Sri Lanka?**
2. Ask a follow-up: **Which of those sectors have the strongest export potential?**
3. Expand the sources displayed beneath the answer.
4. Show the LangSmith Agent trace and explain contextualization, tool selection, retrieval and reranking.
5. Upload a clear land-plan PDF or image in Land Intelligence.
6. Review extracted evidence, location confidence, nearby places, opportunities, risks and verification gaps.
7. Select **Ask Business Advisor about this land** and ask which opportunities appear most suitable.
8. Show the complete Land Intelligence trace.
9. Present the 30-question benchmark, including the measured limitations.

## Known limitations

- The benchmark currently measures retrieval more comprehensively than end-to-end answer correctness.
- The cross-encoder requires domain-specific tuning; it trails the vector-only baseline on the current dataset.
- Statistics and tax/compliance need stronger source coverage.
- OpenStreetMap completeness varies by location, and geocoding may return a broad administrative match.
- Land recommendations are decision support, not legal, valuation, surveying, planning, or investment advice.
- OCR/vision accuracy depends on scan quality and document legibility.

## Deployment

Local browser deployment satisfies the course requirement. A publicly reachable application URL is optional. The local frontend runs at `http://localhost:3000` and the API at `http://localhost:8000`.

The API and frontend can be deployed separately, with the backend connected to a production PostgreSQL/pgvector database. Configure these environment variables on the hosting platforms:

```text
Frontend:
NEXT_PUBLIC_API_URL=https://your-api-host.example

Backend:
CORS_ORIGINS=https://your-frontend-host.example
DATABASE_URL=your-production-postgresql-pgvector-url
OPENAI_API_KEY=your-production-secret
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-production-secret
```

For multiple allowed frontends, provide comma-separated values in `CORS_ORIGINS`. Do not add trailing slashes. The document collection must be ingested into the production database before the RAG endpoints are tested.

If publicly hosting the application, record the frontend and API URLs here and verify Ask AI, conversation history, sources, land upload, and Business Advisor from that deployment.

## Final submission materials

All prepared deliverables are available in [submission](submission/README.md):

- [Four-page report PDF](submission/Sri_Lanka_BI_Copilot_Report_4_pages.pdf) and [editable Word report](submission/Sri_Lanka_BI_Copilot_Report_4_pages.docx)
- [Final presentation](submission/Sri_Lanka_Business_Intelligence_Copilot_Final_2026-09-04_v2.pptx) and [presentation clarifications](submission/PRESENTATION_CORRECTIONS.md)
- [Agent trace and interface evidence](submission/evidence/)
- [Retrieval evaluation report](submission/evidence/evaluation_summary.md), detailed results and benchmark datasets
- [Submission audit and verification notes](submission/SUBMISSION_CHECKLIST.md)

The report follows the requested four-page length. The original brief contains a three-page maximum annotation, so confirm the accepted limit before submitting the report.

## Responsible use

The copilot distinguishes sourced evidence from AI inference and exposes uncertainty where available. Users should verify legal ownership, boundaries, zoning, access, utilities, environmental constraints, taxes, permits, and financial assumptions with qualified professionals before making a decision.
