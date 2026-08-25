from app.rag.rag_pipeline import RAGPipeline


class RAGAgent:

    def __init__(self, pipeline: RAGPipeline | None = None):
        self.pipeline = pipeline or RAGPipeline()


    def run(
        self,
        question: str,
        conversation_id: int | None = None,
    ):

        return self.pipeline.ask(
            question,
            conversation_id=conversation_id,
        )
