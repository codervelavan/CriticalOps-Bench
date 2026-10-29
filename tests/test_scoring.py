from core.scoring import score_use_case


def test_high_readiness_use_case_scores_higher_than_low_readiness():
    high = {
        "name": "SOP retrieval", "business_problem": "Find approved procedures faster",
        "business_value": 5, "technical_feasibility": 5, "data_readiness": 5,
        "governance_readiness": 5, "scalability": 4, "implementation_effort": 1,
    }
    low = {**high, "name": "Autonomous repair", "business_value": 4,
           "technical_feasibility": 2, "data_readiness": 1,
           "governance_readiness": 1, "scalability": 2, "implementation_effort": 5}
    assert score_use_case(high)["score"] > score_use_case(low)["score"]
    assert "human approval" in " ".join(score_use_case(low)["risks_and_next_steps"]).lower() or score_use_case(low)["score"] < 60


def test_invalid_score_rejected():
    data = {
        "name": "bad", "business_value": 6, "technical_feasibility": 3,
        "data_readiness": 3, "governance_readiness": 3, "scalability": 3,
        "implementation_effort": 3,
    }
    try:
        score_use_case(data)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for a score outside 1-5")
