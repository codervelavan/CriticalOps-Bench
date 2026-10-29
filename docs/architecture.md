# Architecture

## Logical flow

```text
Business problem / analyst ticket
              |
              v
  Use-case assessment rubric -----> pilot recommendation + readiness gaps
              |
              v
      FastAPI service
              |
    validate request/schema
              |
              v
  Rule-based triage baseline ------> category + suggested priority + rationale
              |
              v
  Local knowledge retrieval ------> article IDs + evidence score
              |
              v
  Draft recommendation + fallback (offline template by default; optional configured LLM adapter)
              |
              v
    Human review queue -----------> approve / reject / request information
              |
              v
 SQLite incident and audit log -----> CSV export -----> Power BI
              |
              v
  Synthetic evaluation cases ------> accuracy and safety-routing checks
```

## Current prototype components

- **UI:** Streamlit (`app.py`) for use-case scoring, ticket triage, human review, evaluation and operational metrics.
- **API:** FastAPI (`api.py`) exposes JSON endpoints and interactive OpenAPI documentation.
- **Domain logic:** `core/scoring.py`, `core/triage.py`, and `core/knowledge.py`. Optional grounded generation is isolated in `core/generation.py` and activated only when an OpenAI-compatible endpoint is configured.
- **Knowledge:** fictional maintenance articles in Markdown.
- **Storage:** SQLite incident and audit-event log; synthetic reference data in JSON/CSV.
- **Analytics:** exportable incident log plus Power BI-ready synthetic CSV and DAX examples.
- **Tests:** unit tests cover scoring, triage, evaluation safety escalation and API basics.

## Operational context / ontology-inspired model

This demo models a small operational context rather than a full knowledge graph:

- **Entities:** Asset, Incident, KnowledgeArticle, MaintenanceTeam, ReviewDecision.
- **Relationships:** Asset `has_incident` Incident; Incident `references` KnowledgeArticle; Incident `routed_to` MaintenanceTeam; Recommendation `requires_review` ReviewDecision.
- **Rules:** safety concerns route to critical review; the approved site policy overrides the prototype; low evidence triggers fallback; only an authorised human reviewer records approval.
- **Permissions:** this demo uses reviewer labels only and is not identity-secured. Real deployment must enforce authenticated identities and resource-level access control in the backend.
- **Possible actions:** draft response, route recommendation, request information, record review. No equipment-control action exists.

This is inspired by the public description of Atos Codex's operational ontology and governed actions, but it is not a reproduction of Atos Codex or Genesis Intelligence.

## Proposed production evolution

1. Replace lexical retrieval with a measured hybrid retrieval pipeline (keyword + embeddings), including document ownership, freshness and version metadata.
2. Add approved enterprise knowledge connectors and enforce source permissions at retrieval time.
3. Introduce a provider-neutral model adapter with policy-based model routing; log model/version, latency, token counts and estimated cost.
4. Add proper identity and roles, central secrets management, TLS, audit retention and deployment controls.
5. Integrate with a sandboxed ticketing system through a custom connector or REST adapter. Keep state-changing actions behind explicit approval.
6. Add continuous evaluations, prompt-injection tests, data leakage checks, observability, red-team scenarios and staged rollout.
7. Deploy according to data-sovereignty and workload requirements (cloud, private/sovereign environment or on-premises); make that a client constraint rather than assuming one deployment model.

## Failure handling

- Invalid payload: schema validation error.
- No relevant article: fallback and human escalation.
- Safety flag or danger terms: critical review and no automated action.
- No reviewer decision: remains pending.
- Storage failure: the API should return an error; future production implementation should add retries/monitoring without losing audit records.
