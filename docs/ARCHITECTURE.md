# Architecture and components

## RAG path

The API routes a question to `RAGPipeline`. Conversation history can contextualize follow-up questions. An OpenAI embedding queries PostgreSQL/pgvector for 20 candidates; a cross encoder reranks them, and the best three chunks become grounded context for the answer model. Returned sources retain document and chunk metadata.

The deliberately simpler evaluation baseline stops after vector similarity and takes its first three results. The production path reranks the same 20 candidates, making the comparison controlled and interpretable.

## Land Intelligence path

`LandAgent` orchestrates six evidence-producing capabilities:

1. The document parser turns a supported PDF or image into page images.
2. Vision extraction returns structured observations from each page.
3. Location normalization converts visible address fragments into a Sri Lanka-focused search query.
4. Nominatim returns a coordinate, match level, and confidence; a failed lookup does not stop document analysis.
5. Overpass provides nearby roads and amenities with coordinates and straight-line distances.
6. Business analysis and report building separate evidence, opportunities, risks, and missing verification.

Land evidence can also be passed to the Business Advisor context so recommendations can combine property observations with retrieved business knowledge.

## Agent behavior and resilience

The application exposes RAG and Land Agent routes rather than hiding all work in a single prompt. The Land Agent decides conditionally: it normalizes and geocodes only when the vision result contains location evidence, but it always attempts a survey-grounded business assessment. External geocoding or nearby-service failure returns explicit empty/fallback data instead of aborting the complete analysis.

`AgentRouter.run` is the model-directed interaction path. A structured LLM decision selects `knowledge_search` or `business_advisor` from the contextualized question, conversation history, and presence of a land report. The parent run, routing decision, selected tool, and downstream RAG/advisor spans are traceable. Existing focused endpoints remain available; `/agent` is the unified agent route.

## Observability

LangSmith records a parent `Land Intelligence Analysis` run and named nested spans for every component. The separate `Nearby OpenStreetMap Intelligence` span makes the tool call, latency, empty response, or network error visible under geolocation. RAG retrieval, reranking, and pipeline runs are traced independently.

## Security and operational notes

Secrets belong in environment variables and must not be committed. Uploaded documents may contain property and personal information; production deployments should add authenticated access, retention limits, encrypted storage, request-size limits, rate limits, and a documented deletion policy. Public geocoding services also impose acceptable-use and rate-limit requirements.
