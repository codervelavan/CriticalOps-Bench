from typing import Any, Dict


def score_use_case(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transparent weighted score for early use-case triage; not an investment decision."""
    weights = {
        "business_value": 0.30,
        "technical_feasibility": 0.20,
        "data_readiness": 0.20,
        "governance_readiness": 0.15,
        "scalability": 0.15,
    }
    missing = [key for key in weights if key not in data]
    if missing:
        raise ValueError(f"Missing scoring fields: {', '.join(missing)}")
    for key in list(weights) + ["implementation_effort"]:
        value = int(data[key])
        if not 1 <= value <= 5:
            raise ValueError(f"{key} must be between 1 and 5")

    weighted_mean = sum(float(data[k]) * weight for k, weight in weights.items())
    raw_score = weighted_mean / 5 * 100
    effort_penalty = (int(data.get("implementation_effort", 3)) - 1) * 3.0
    score = round(max(0, min(100, raw_score - effort_penalty)), 1)
    if score >= 75:
        recommendation = "Prioritise for a controlled pilot"
    elif score >= 60:
        recommendation = "Run focused discovery and close readiness gaps"
    else:
        recommendation = "Defer, reduce scope, or redesign"

    risks = []
    if int(data["data_readiness"]) <= 2:
        risks.append("Data readiness is low: validate availability, quality, ownership and permissions before prototyping.")
    if int(data["governance_readiness"]) <= 2:
        risks.append("Governance readiness is low: define access control, human approval, audit and escalation before pilot.")
    if int(data["technical_feasibility"]) <= 2:
        risks.append("Technical feasibility is uncertain: run a small technical spike before committing to a build.")
    if int(data.get("implementation_effort", 3)) >= 4:
        risks.append("Implementation effort is high: split the use case into a smaller measurable first release.")
    if not risks:
        risks.append("No low-scoring readiness dimension was identified by this rubric; validate all assumptions with stakeholders.")

    return {
        "name": data.get("name", "Unnamed use case"),
        "score": score,
        "recommendation": recommendation,
        "score_breakdown": {k: round(float(data[k]) * weight / 5 * 100, 1) for k, weight in weights.items()},
        "effort_penalty_points": round(effort_penalty, 1),
        "risks_and_next_steps": risks,
        "disclaimer": "A discovery aid for prioritisation, not a substitute for a validated business case or risk review.",
    }


def demo_use_cases():
    examples = [
        {
            "name": "Maintenance incident triage and SOP retrieval",
            "business_problem": "Maintenance teams manually classify equipment issues and search work instructions.",
            "business_value": 5, "technical_feasibility": 4, "data_readiness": 4,
            "governance_readiness": 4, "scalability": 4, "implementation_effort": 3,
        },
        {
            "name": "Fully autonomous repair execution",
            "business_problem": "Automatically issue commands to machinery and perform physical interventions.",
            "business_value": 4, "technical_feasibility": 2, "data_readiness": 2,
            "governance_readiness": 1, "scalability": 2, "implementation_effort": 5,
        },
        {
            "name": "Maintenance knowledge assistant with approval",
            "business_problem": "Help analysts find approved SOPs and draft a response with source evidence.",
            "business_value": 4, "technical_feasibility": 5, "data_readiness": 4,
            "governance_readiness": 4, "scalability": 4, "implementation_effort": 2,
        },
    ]
    return [{**item, "assessment": score_use_case(item)} for item in examples]
