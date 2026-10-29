"""Generate the fully synthetic Power BI input CSV from labelled evaluation cases."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from core.evaluation import load_cases, run_evaluation
from core.triage import triage_incident

rows = []
for i, case in enumerate(load_cases(), start=1):
    result = triage_incident(case["input"])
    rows.append({
        "incident_id": case["case_id"],
        "created_date": f"2026-10-{((i - 1) % 27) + 1:02d}",
        "site": case["input"].get("site", "Demo Site"),
        "asset_id": case["input"].get("asset_id", "ASSET-UNKNOWN"),
        "category_expected": case["expected_category"],
        "category_predicted": result["category"],
        "category_pass": result["category"] == case["expected_category"],
        "priority_expected": case["expected_priority"],
        "priority_predicted": result["suggested_priority"],
        "priority_pass": result["suggested_priority"] == case["expected_priority"],
        "safety_expected": bool(case.get("safety_expected", case["input"].get("safety_related", False))),
        "safety_escalation_pass": (not bool(case.get("safety_expected", case["input"].get("safety_related", False)))) or (result["suggested_priority"] == "critical_review" and result["human_review_required"]),
        "production_impact": case["input"].get("production_impact", 3),
        "downtime_hours": case["input"].get("estimated_downtime_hours", 0),
        "retrieval_confidence": result["retrieval_confidence"],
        "fallback_used": result["fallback_used"],
        "retrieved_articles": ";".join(s["article_id"] for s in result["retrieved_sources"]),
        "review_status": "synthetic_pending",
        "model_mode": result["model_mode"],
        "data_type": "SYNTHETIC_DEMO",
    })

out = ROOT / "powerbi" / "sample_incidents.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"Wrote {len(rows)} synthetic rows to {out}")
