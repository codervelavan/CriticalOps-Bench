import os
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from core.evaluation import run_evaluation
from core.schemas import IncidentRequest, ReviewRequest, UseCaseAssessment, IncidentResponse, AuditEvent, MetricsResponse, ErrorResponse
from core.scoring import demo_use_cases, score_use_case
from core.store import ReviewConflict, get_incident, audit_history, init_db, list_incidents, metrics_summary, review_incident, save_incident
from core.triage import triage_incident

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="CriticalOps AI Workbench API",
    description="Portfolio demo for use-case assessment, grounded decision support, human review and evaluation.",
    version="0.2.0",
    lifespan=lifespan,
)


@app.get("/health", operation_id="getHealth")
def health():
    return {"status": "ok", "mode": "llm-configured" if all(os.getenv(k) for k in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL")) else "offline-template-demo", "note": "Synthetic portfolio prototype; not an operational safety system."}


@app.get("/api/use-cases", operation_id="listUseCases")
def use_cases():
    return demo_use_cases()


@app.post("/api/use-cases/score", operation_id="scoreUseCase")
def score(data: UseCaseAssessment):
    try:
        return score_use_case(data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/incidents/triage", operation_id="triageIncident", response_model=IncidentResponse, responses={409: {"model": ErrorResponse, "description": "Incident ID already exists"}})
def triage(data: IncidentRequest):
    ticket = data.model_dump()
    result = triage_incident(ticket)
    try:
        return save_incident(ticket, result)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Incident ID already exists") from exc


@app.get("/api/incidents", operation_id="listIncidents", response_model=list[IncidentResponse])
def incidents(limit: int = 200):
    return list_incidents(limit)


@app.post("/api/incidents/{incident_id}/review", operation_id="reviewIncident", response_model=IncidentResponse, responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse, "description": "Stale or finalised review"}})
def review(incident_id: str, data: ReviewRequest):
    try:
        result = review_incident(incident_id, data.decision, data.reviewer, data.comment, data.expected_version)
    except ReviewConflict as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return result


@app.post("/api/evaluate", operation_id="evaluateBaseline")
def evaluate():
    return run_evaluation()


@app.get("/api/metrics", operation_id="getMetrics", response_model=MetricsResponse)
def metrics():
    return metrics_summary()


@app.get("/api/incidents/{incident_id}", operation_id="getIncident", response_model=IncidentResponse, responses={404: {"model": ErrorResponse}})
def incident_detail(incident_id: str):
    result = get_incident(incident_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return result


@app.get("/api/incidents/{incident_id}/audit", operation_id="getIncidentAudit", response_model=list[AuditEvent], responses={404: {"model": ErrorResponse}})
def incident_audit(incident_id: str):
    if get_incident(incident_id) is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return audit_history(incident_id)
