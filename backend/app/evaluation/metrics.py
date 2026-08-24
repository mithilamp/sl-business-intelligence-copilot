from typing import Any


def _metadata_text(retrieved_source: dict[str, Any]) -> str:
    return " ".join(
        str(value)
        for value in retrieved_source.values()
        if value is not None
    )


def source_hit(
    expected_sources: list[str],
    retrieved_sources: list[dict[str, Any]],
) -> bool:

    retrieved_text = " ".join(
        _metadata_text(source)
        for source in retrieved_sources
    ).lower()


    for expected in expected_sources:

        if expected.lower() in retrieved_text:
            return True


    return False



def calculate_source_hit_rate(
    results: list[dict],
):

    if not results:
        return 0


    hits = 0


    for result in results:

        if source_hit(
            result["expected_sources"],
            result["retrieved_sources"],
        ):
            hits += 1


    return round(
        hits / len(results),
        3,
    )



def category_summary(
    results: list[dict],
):

    summary = {}


    for result in results:

        category = result["category"]


        if category not in summary:

            summary[category] = {
                "total": 0,
                "hits": 0,
            }


        summary[category]["total"] += 1


        if source_hit(
            result["expected_sources"],
            result["retrieved_sources"],
        ):

            summary[category]["hits"] += 1



    for category, data in summary.items():

        data["hit_rate"] = round(
            data["hits"] / data["total"],
            3,
        )


    return summary
