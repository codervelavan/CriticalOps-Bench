from core.triage import triage_incident


def test_vibration_ticket_gets_category_and_review():
    out = triage_incident({
        "description": "Pump vibration is increasing and bearing noise started this morning",
        "asset_id": "PUMP-204", "production_impact": 3,
        "estimated_downtime_hours": 1, "safety_related": False,
    })
    assert out["category"] == "vibration_or_bearing"
    assert out["human_review_required"] is True
    assert out["review_status"] == "pending"
    assert out["model_mode"] == "offline-template-demo"


def test_safety_issue_is_escalated_and_never_auto_acted():
    out = triage_incident({
        "description": "Smoke is visible near the motor housing",
        "asset_id": "MOTOR-12", "production_impact": 5,
        "estimated_downtime_hours": 0, "safety_related": False,
    })
    assert out["suggested_priority"] == "critical_review"
    assert out["suggested_queue"] == "Safety / Operations Lead"
    assert out["human_review_required"] is True


def test_no_evidence_uses_fallback():
    out = triage_incident({
        "description": "Unrecognised issue with a strange status lamp",
        "asset_id": "ASSET-UNKNOWN", "production_impact": 2,
        "estimated_downtime_hours": 0, "safety_related": False,
    })
    assert out["fallback_used"] is True
