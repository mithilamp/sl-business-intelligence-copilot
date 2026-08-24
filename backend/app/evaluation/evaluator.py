import json
from pathlib import Path

from app.rag.rag_pipeline import RAGPipeline


class RAGEvaluator:

    def __init__(self):

        self.pipeline = RAGPipeline()


    def load_questions(self):

        path = (
            Path(__file__)
            .parent
            / "datasets"
            / "benchmark_questions.json"
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    def run(self):

        questions = self.load_questions()

        results = []


        for item in questions:

            response = self.pipeline.ask(
                item["question"]
            )


            results.append(
                {
                    "id": item["id"],

                    "question":
                        item["question"],

                    "category":
                        item["category"],

                    "expected_sources":
                        item["expected_sources"],

                    "retrieved_sources":
                        [
                            {
                                "title": source.title,
                                "filename": source.filename,
                                "source": source.source,
                                "category": source.category,
                                "document_type": source.document_type,
                                "published_date": source.published_date,
                                "document_url": source.document_url,
                            }
                            for source in response.sources
                        ],

                    "answer":
                        response.answer
                }
            )


        return results
