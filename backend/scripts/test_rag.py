from app.rag.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

answer = pipeline.ask(
    "What is the minimum capital requirement for opening a new bank?"
)

print(answer)