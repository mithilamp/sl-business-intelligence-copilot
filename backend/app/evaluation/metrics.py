"""Deterministic, metadata-aware retrieval metrics."""

from collections import defaultdict
from typing import Any


def _normalise(value: Any) -> str:
    return " ".join(str(value or "").lower().replace("&", "and").split())


def source_matches(expected: str, source: dict[str, Any]) -> bool:
    haystack = _normalise(" ".join(str(value) for value in source.values() if value))
    return any(_normalise(alias) in haystack for alias in expected.split("|") if alias)


def matched_ranks(expected_sources: list[str], retrieved_sources: list[dict[str, Any]]) -> list[int]:
    return [rank for rank, source in enumerate(retrieved_sources, 1)
            if any(source_matches(expected, source) for expected in expected_sources)]


def source_hit(expected_sources: list[str], retrieved_sources: list[dict[str, Any]]) -> bool:
    return bool(matched_ranks(expected_sources, retrieved_sources))


def reciprocal_rank(expected_sources: list[str], retrieved_sources: list[dict[str, Any]]) -> float:
    ranks = matched_ranks(expected_sources, retrieved_sources)
    return round(1 / min(ranks), 4) if ranks else 0.0


def precision_at_k(expected_sources: list[str], retrieved_sources: list[dict[str, Any]], k: int = 3) -> float:
    if k <= 0:
        return 0.0
    relevant = sum(any(source_matches(expected, source) for expected in expected_sources)
                   for source in retrieved_sources[:k])
    return round(relevant / k, 4)


def annotate_result(result: dict[str, Any], k: int = 3) -> dict[str, Any]:
    ranks = matched_ranks(result["expected_sources"], result["retrieved_sources"])
    annotated = dict(result)
    annotated["metrics"] = {
        f"hit_at_{k}": any(rank <= k for rank in ranks),
        "first_relevant_rank": min(ranks) if ranks else None,
        "reciprocal_rank": reciprocal_rank(result["expected_sources"], result["retrieved_sources"]),
        f"precision_at_{k}": precision_at_k(result["expected_sources"], result["retrieved_sources"], k),
    }
    if not ranks:
        annotated["failure"] = {
            "type": "expected_source_not_retrieved",
            "expected_sources": result["expected_sources"],
            "returned_authorities": sorted({source.get("source") or "unknown" for source in result["retrieved_sources"]}),
        }
    return annotated


def summarise(results: list[dict[str, Any]], k: int = 3) -> dict[str, Any]:
    annotated = [annotate_result(result, k) for result in results]
    total = len(annotated)
    categories: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in annotated:
        categories[item["category"]].append(item)
    hits = sum(item["metrics"][f"hit_at_{k}"] for item in annotated)
    return {
        "total": total,
        f"hit_rate_at_{k}": round(hits / total, 4) if total else 0.0,
        "mean_reciprocal_rank": round(sum(item["metrics"]["reciprocal_rank"] for item in annotated) / total, 4) if total else 0.0,
        f"mean_precision_at_{k}": round(sum(item["metrics"][f"precision_at_{k}"] for item in annotated) / total, 4) if total else 0.0,
        "failures": [item for item in annotated if item.get("failure")],
        "category_summary": {
            category: {"total": len(items), "hits": sum(item["metrics"][f"hit_at_{k}"] for item in items),
                       f"hit_rate_at_{k}": round(sum(item["metrics"][f"hit_at_{k}"] for item in items) / len(items), 4)}
            for category, items in sorted(categories.items())
        },
        "results": annotated,
    }


def calculate_source_hit_rate(results: list[dict]) -> float:
    return summarise(results)["hit_rate_at_3"]


def category_summary(results: list[dict]) -> dict:
    summary = summarise(results)["category_summary"]
    return {key: {**value, "hit_rate": value["hit_rate_at_3"]} for key, value in summary.items()}
