import json
from pathlib import Path
from typing import Any, Dict, List
from core.triage import triage_incident

ROOT = Path(__file__).resolve().parents[1]
EVAL_FILE = ROOT / "data" / "demo" / "evaluation_cases.json"


def load_cases() -> List[Dict[str, Any]]:
    return json.loads(EVAL_FILE.read_text(encoding="utf-8"))


def run_evaluation(cases: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    cases = cases if cases is not None else load_cases()
    rows = []
    category_matches = 0
    priority_matches = 0
    safety_cases = 0
    safety_raised = 0
    fallback_cases = 0
    retrieval_hits = []
    reciprocal_ranks = []
    fallback_labels = []
    for case in cases:
        request = case["input"]
        output = triage_incident(request, use_model=False)
        category_ok = output["category"] == case["expected_category"]
        priority_ok = output["suggested_priority"] == case["expected_priority"]
        if category_ok:
            category_matches += 1
        if priority_ok:
            priority_matches += 1
        if request.get("safety_related") or case.get("safety_expected"):
            safety_cases += 1
            if output["suggested_priority"] == "critical_review" and output["human_review_required"]:
                safety_raised += 1
        if output["fallback_used"]:
            fallback_cases += 1
        expected_articles = case.get("expected_article_ids")
        retrieved_ids = [s["article_id"] for s in output["retrieved_sources"]]
        hit = None
        rank = None
        if expected_articles:
            rank = next((i + 1 for i, article in enumerate(retrieved_ids[:3]) if article in expected_articles), None)
            hit = rank is not None
            retrieval_hits.append(int(hit))
            reciprocal_ranks.append(1 / rank if rank else 0)
        if "expected_fallback" in case:
            fallback_labels.append((bool(case["expected_fallback"]), output["fallback_used"]))
        rows.append({
            "case_id": case["case_id"],
            "expected_article_ids": expected_articles,
            "retrieval_hit_at_3": hit,
            "first_relevant_rank": rank,
            "expected_fallback": case.get("expected_fallback"),
            "description": request["description"],
            "expected_category": case["expected_category"],
            "predicted_category": output["category"],
            "category_pass": category_ok,
            "expected_priority": case["expected_priority"],
            "predicted_priority": output["suggested_priority"],
            "priority_pass": priority_ok,
            "fallback_used": output["fallback_used"],
            "sources": ", ".join(s["article_id"] for s in output["retrieved_sources"]),
        })
    n = max(1, len(cases))
    tp = sum(expected and actual for expected, actual in fallback_labels)
    predicted = sum(actual for _, actual in fallback_labels)
    expected = sum(label for label, _ in fallback_labels)

    return {
        "cases_run": len(cases),
        "category_matches": category_matches,
        "priority_matches": priority_matches,
        "safety_cases": safety_cases,
        "safety_escalations": safety_raised,
        "retrieval_cases_labelled": len(retrieval_hits),
        "retrieval_hits_at_3": sum(retrieval_hits),
        "retrieval_hit_at_3_pct": round(sum(retrieval_hits) / len(retrieval_hits) * 100, 1) if retrieval_hits else None,
        "mean_reciprocal_rank_at_3": round(sum(reciprocal_ranks) / len(reciprocal_ranks), 4) if reciprocal_ranks else None,
        "fallback_labelled_cases": len(fallback_labels),
        "fallback_true_positives": tp,
        "fallback_predicted_positives": predicted,
        "fallback_expected_positives": expected,
        "fallback_precision": round(tp / predicted, 4) if predicted else None,
        "fallback_recall": round(tp / expected, 4) if expected else None,
        "generation_evaluation": "Not run: deterministic evaluation disables all external model calls",

        "category_exact_match_pct": round(category_matches / n * 100, 1),
        "priority_exact_match_pct": round(priority_matches / n * 100, 1),
        "safety_escalation_pass_pct": round(safety_raised / max(1, safety_cases) * 100, 1),
        "fallback_cases": fallback_cases,
        "results": rows,
        "interpretation": "Synthetic offline evaluation of the current rule-and-keyword baseline. These scores are not evidence of production performance and should not be represented as client outcomes.",
    }
