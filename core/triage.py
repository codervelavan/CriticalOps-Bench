from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid
from core.knowledge import retrieve
from core.generation import generate_grounded_response

CATEGORY_TERMS = {
    "vibration_or_bearing": {"vibration", "bearing", "noise", "shaft", "misalignment"},
    "overheating": {"overheat", "overheating", "hot", "temperature", "smoke", "burning"},
    "leak_or_pressure": {"leak", "leaking", "leakage", "fluid", "pressure", "spill", "seal"},
    "conveyor_or_blockage": {"conveyor", "jam", "jammed", "belt", "blockage", "stuck"},
    "sensor_or_data_quality": {"sensor", "telemetry", "reading", "spike", "missing", "drift", "inconsistent"},
}


def _classify(text: str) -> str:
    normalized = text.lower()
    token_hits = {}
    for category, terms in CATEGORY_TERMS.items():
        token_hits[category] = sum(1 for term in terms if term in normalized)
    best = max(token_hits, key=token_hits.get)
    return best if token_hits[best] else "general_maintenance"


def _priority(request: Dict[str, Any], text: str) -> tuple[str, str]:
    normalized = text.lower()
    immediate_hazards = ["smoke", "fire", "injury", "burning smell", "electrical arc", "unknown chemical"]
    if request.get("safety_related") or any(term in normalized for term in immediate_hazards):
        return "critical_review", "Potential safety concern: follow the site's emergency procedure and alert the authorised safety/operations team. Do not rely on this prototype for operational instructions."
    impact = int(request.get("production_impact", 3))
    downtime = float(request.get("estimated_downtime_hours", 0))
    if impact >= 5 or downtime >= 8:
        return "high", "High production impact or extended downtime was reported; route to the responsible maintenance lead for priority confirmation."
    if impact >= 4 or downtime >= 2:
        return "medium_high", "Operational impact may be significant; verify against the site's approved priority policy."
    if impact <= 2 and downtime < 1:
        return "low", "Reported impact is limited; confirm that no safety or service-level condition changes the priority."
    return "medium", "Confirm impact and urgency with the reporter and compare with the approved site policy."


def triage_incident(request: Dict[str, Any]) -> Dict[str, Any]:
    description = str(request.get("description", "")).strip()
    category = _classify(description)
    priority, priority_reason = _priority(request, description)
    query = description
    articles = retrieve(query, top_k=3)
    best_score = float(articles[0]["score"]) if articles else 0.0
    sources = [
        {"article_id": item["article_id"], "title": item["title"], "retrieval_score": item["score"]}
        for item in articles
    ]
    if articles and best_score >= 0.15:
        evidence_message = (
            f"Potentially relevant approved demo knowledge: {articles[0]['title']} ({articles[0]['article_id']}). "
            "Review the cited material and the actual site procedure before deciding what to do."
        )
        fallback_used = False
    else:
        evidence_message = "I could not retrieve sufficiently relevant evidence. Request more information or route to a qualified maintenance analyst."
        fallback_used = True
    if priority == "critical_review":
        queue = "Safety / Operations Lead"
        action = "Human safety review required; no automated operational action permitted."
    elif category == "sensor_or_data_quality":
        queue = "Instrumentation / Data Quality"
        action = "Validate timestamp, units, asset mapping, and reading quality before drawing conclusions."
    elif category == "general_maintenance":
        queue = "Maintenance Triage"
        action = "Ask for asset ID, symptoms, start time, and operational impact; then route to a qualified reviewer."
    else:
        queue = "Mechanical Maintenance"
        action = "Review retrieved SOP evidence and asset history; a qualified person determines any intervention."

    # The default is an offline deterministic template. An optional configured
    # OpenAI-compatible endpoint may draft a grounded response when evidence exists.
    fallback_draft = (
        f"Suggested category: {category.replace('_', ' ')}. Suggested priority: {priority}. "
        f"Reason: {priority_reason} {evidence_message} "
        "Please confirm the asset details and follow the approved site procedure. This is a decision-support draft, not an instruction to operate, stop, isolate, or repair equipment."
    )
    # Potential safety cases never call a model for a suggested operational response.
    if priority == "critical_review" or fallback_used:
        generation = {"text": fallback_draft, "mode": "offline-template-demo", "error": ""}
    else:
        generation = generate_grounded_response(
            description=description, category=category, priority=priority,
            priority_reason=priority_reason, queue=queue, next_step=action,
            articles=articles, fallback_message=fallback_draft,
        )
    draft = generation["text"]
    return {
        "incident_id": request.get("incident_id") or f"INC-{uuid.uuid4().hex[:8].upper()}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "asset_id": request.get("asset_id", "ASSET-UNKNOWN"),
        "site": request.get("site", "Demo Site"),
        "category": category,
        "suggested_priority": priority,
        "priority_reason": priority_reason,
        "suggested_queue": queue,
        "suggested_next_step": action,
        "retrieved_sources": sources,
        "retrieval_mode": "keyword-baseline",
        "retrieval_confidence": round(best_score, 3),
        "fallback_used": fallback_used,
        "draft_response": draft,
        "human_review_required": True,
        "review_status": "pending",
        "model_mode": generation["mode"],
        "generation_error": generation["error"],
        "disclaimer": "Synthetic portfolio demonstration only. Not an operational safety system. Always follow approved site procedures and qualified human judgment.",
    }
