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
    for case in cases:
        request = case["input"]
        output = triage_incident(request)
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
        rows.append({
            "case_id": case["case_id"],
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
    return {
        "cases_run": len(cases),
        "category_exact_match_pct": round(category_matches / n * 100, 1),
        "priority_exact_match_pct": round(priority_matches / n * 100, 1),
        "safety_escalation_pass_pct": round(safety_raised / max(1, safety_cases) * 100, 1),
        "fallback_cases": fallback_cases,
        "results": rows,
        "interpretation": "Synthetic offline evaluation of the current rule-and-keyword baseline. These scores are not evidence of production performance and should not be represented as client outcomes.",
    }
