# Final demo guide

## Before presenting

- Start PostgreSQL, backend, and frontend; verify the configured corpus is populated.
- Run the benchmark and keep `evaluation_summary.md` open.
- Enable LangSmith and perform one rehearsal land upload so the project and trace are easy to find.
- Use a clear, consented land document with a readable location and keep a fallback sample ready.

## Suggested 8-minute product demo

1. Ask: “Which sectors are promoted for foreign investment in Sri Lanka?” Point out the answer and publisher/document citations.
2. Ask a contextual follow-up in the same conversation to demonstrate memory, then reopen it from question history.
3. In the API documentation, call `POST /agent` and show the selected tool and routing reason.
4. Upload the land plan. While it runs, explain that the model is extracting visible evidence rather than treating the PDF as plain text.
5. Show property evidence, geocode confidence/location level, nearby infrastructure and distances, opportunities, risks, and verification gaps.
6. Open the LangSmith parent trace. Expand the routing decision, parser, vision, normalization, geolocation, nearby intelligence, business analysis, and report spans.
7. Show the evaluation table: 30 RAG questions, the vector-only baseline, reranked production results, answer-quality rubric, category breakdown, and honest failures.

## Closing statement

The system is a screening and research copilot. It grounds business answers in source documents and combines observable land evidence with geospatial context, but it does not replace a licensed surveyor, lawyer, tax adviser, valuer, or investment professional.
