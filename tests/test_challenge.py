import json
from pathlib import Path
from core.evaluation import run_evaluation


def test_challenge_counts_and_retrieval_metrics():
    cases = json.loads((Path(__file__).resolve().parents[1] / "data/demo/challenge_cases.json").read_text())
    assert len(cases) == 36
    assert len({case["case_id"] for case in cases}) == 36
    report = run_evaluation(cases)
    assert report["retrieval_cases_labelled"] == 30
    assert report["fallback_labelled_cases"] == 36
    assert report["fallback_expected_positives"] == 6
    assert report["category_matches"] == sum(row["category_pass"] for row in report["results"])
    assert report["retrieval_hits_at_3"] == sum(row["retrieval_hit_at_3"] is True for row in report["results"])
    assert 0 <= report["mean_reciprocal_rank_at_3"] <= 1
    assert report["generation_evaluation"].startswith("Not run")


def test_unlabelled_retrieval_is_not_reported_as_zero():
    report = run_evaluation([])
    assert report["cases_run"] == 0
    assert report["retrieval_hit_at_3_pct"] is None
    assert report["fallback_precision"] is None
