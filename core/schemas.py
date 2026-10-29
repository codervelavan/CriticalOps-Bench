from typing import Literal, Optional
from pydantic import BaseModel, Field


class UseCaseAssessment(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    business_problem: str = Field(min_length=8, max_length=1000)
    business_value: int = Field(ge=1, le=5, description="1=low, 5=high")
    technical_feasibility: int = Field(ge=1, le=5)
    data_readiness: int = Field(ge=1, le=5)
    governance_readiness: int = Field(ge=1, le=5)
    scalability: int = Field(ge=1, le=5)
    implementation_effort: int = Field(ge=1, le=5, description="1=low effort, 5=high effort")


class IncidentRequest(BaseModel):
    incident_id: Optional[str] = Field(default=None, max_length=40)
    description: str = Field(min_length=8, max_length=2000)
    asset_id: str = Field(default="ASSET-UNKNOWN", max_length=80)
    site: str = Field(default="Demo Site", max_length=120)
    production_impact: int = Field(default=3, ge=1, le=5)
    estimated_downtime_hours: float = Field(default=0, ge=0, le=10000)
    safety_related: bool = False


class ReviewRequest(BaseModel):
    expected_version: int = Field(default=0, ge=0, description="Version displayed when the review was loaded; stale or finalised reviews return 409")
    decision: Literal["approved", "rejected", "needs_more_information"]
    reviewer: str = Field(default="Demo Reviewer", min_length=2, max_length=100)
    comment: str = Field(default="", max_length=1000)


class SourceReference(BaseModel):
    article_id: str
    title: str
    retrieval_score: float


class IncidentResponse(BaseModel):
    incident_id: str
    created_at: str
    asset_id: str
    site: str
    category: str
    suggested_priority: str
    priority_reason: str
    suggested_queue: str
    suggested_next_step: str
    retrieved_sources: list[SourceReference]
    retrieval_mode: str
    retrieval_confidence: float
    fallback_used: bool
    draft_response: str
    human_review_required: bool
    review_status: Literal["pending", "approved", "rejected", "needs_more_information"]
    model_mode: str
    generation_error: str
    disclaimer: str
    version: int = 0
    reviewer: Optional[str] = None
    review_comment: Optional[str] = None
    reviewed_at: Optional[str] = None
    ticket: Optional[dict] = None


class AuditEvent(BaseModel):
    id: int
    event_time: str
    incident_id: str
    event_type: str
    actor: str
    details: str


class MetricsResponse(BaseModel):
    total_incidents: int
    pending_reviews: int
    critical_reviews: int
    fallback_rate_pct: float
    category_counts: dict[str, int]
    review_counts: dict[str, int]


class ErrorResponse(BaseModel):
    detail: str
