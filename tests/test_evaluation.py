from core.evaluation import run_evaluation


def test_evaluation_reports_results_and_safety_cases():
    report = run_evaluation()
    assert report["cases_run"] >= 13
    assert report["category_exact_match_pct"] >= 0
    assert report["priority_exact_match_pct"] >= 0
    assert report["safety_escalation_pass_pct"] == 100.0
    assert len(report["results"]) == report["cases_run"]
    assert {row["case_id"] for row in report["results"]} >= {"EVAL-013"}
    assert report["generation_evaluation"].startswith("Not run")
    assert "Synthetic" in report["interpretation"]
