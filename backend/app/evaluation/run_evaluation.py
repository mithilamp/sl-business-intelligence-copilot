import json
from pathlib import Path

from app.evaluation.evaluator import RAGEvaluator
from app.evaluation.metrics import (
    calculate_source_hit_rate,
    category_summary,
)


def main():

    evaluator = RAGEvaluator()

    results = evaluator.run()


    report = {

        "total_questions":
            len(results),

        "source_hit_rate":
            calculate_source_hit_rate(
                results
            ),

        "category_summary":
            category_summary(
                results
            ),

        "results":
            results,
    }


    output = (
        Path(__file__)
        .parent
        / "reports"
        / "evaluation_results.json"
    )


    with open(
        output,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )


    print(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()