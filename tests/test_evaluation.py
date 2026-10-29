from core.evaluation import run_evaluation


def test_evaluation_reports_results_and_safety_cases():
    report = run_evaluation()
    assert report["cases_run"] >= 13
    assert report["category_exact_match_pct"] >= 0
    assert report["priority_exact_match_pct"] >= 0
    assert report["safety_escalation_pass_pct"] == 100.0
    assert len(report["results"]) == report["cases_run"]
    assert any(not row["category_pass"] for row in report["results"]), "The suite should expose at least one known edge-case failure"
    assert "Synthetic" in report["interpretation"]
