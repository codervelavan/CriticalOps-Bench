# CriticalOps AI Workbench

[Capability evidence index](evidence/capabilities.md) | [Learning walkthrough](docs/learning_walkthrough.md)

## Verified extension

- Versioned human review, duplicate-intake protection and atomic application audit records.
- Typed incident/detail/review/audit/metrics responses, stable operation IDs and 404/409/422 handling.
- [Locally validated OpenAPI 2.0 connector definition](connectors/README.md).
- [Desktop-verified Power BI report](powerbi/desktop/README.md): two pages, six DAX measures, tested filters and native save/reopen.
- [Original and expanded synthetic evaluation results](evidence/README.md), including failures.
- [As-is/to-be workflow](docs/workflow.md) and [analyst adoption/demo guide](docs/analyst_guide.md).

Install development dependencies with `pip install -r requirements-dev.txt`, run `pytest -q`, then `python scripts/evaluate.py`. GitHub Actions repeats the checks. Existing databases gain a version column without dropping records. Reviewer labels are not authenticated identities; the API remains local-only. Live Power Platform integration is not asserted.

**An independent maintenance decision-support prototype for use-case assessment, incident triage and human review.**

The workbench explores evidence-linked recommendations, review workflows and measurable evaluation using fictional maintenance incidents.

All incidents and procedures in this repository are fictional. The default application uses transparent rules, keyword retrieval and templated responses. An optional OpenAI-compatible chat-completions endpoint can be configured to draft grounded responses when evidence is present; it is disabled by default. The current retriever is keyword-based, not embedding/vector search, and the app does not execute agent actions.

## What problem does it solve?

Maintenance teams may spend time classifying incident descriptions, locating relevant work instructions, identifying missing information and routing requests. The prototype demonstrates how an assistant could provide an evidence-linked triage *suggestion*, retain a human review step, and measure quality in a controlled demo.

## Primary user story

> As a maintenance operations analyst, I want an evidence-linked triage recommendation for an equipment incident so that I can route work consistently and find approved guidance faster, while a qualified human remains responsible for the final decision.

Supporting user stories cover use-case scoring, operational analytics, governance review and API integration. Full acceptance criteria are in [docs/user_stories.md](docs/user_stories.md).

## Features

- **AI opportunity assessment:** transparent weighted scoring across business value, feasibility, data readiness, governance readiness, scalability and implementation effort.
- **Incident triage:** category, suggested priority, rationale, routing queue and next-step suggestion from a short incident description.
- **Local knowledge retrieval:** lexical baseline over fictional approved-demo maintenance articles, with article IDs and an explicit fallback.
- **Human-review queue:** approve, reject or request more information; record reviewer notes and audit events.
- **Evaluation suite:** compare output with labelled synthetic cases; report category and priority exact match and whether safety cases go to review.
- **Operational metrics:** local incident counts, pending reviews, fallback rate and category distribution.
- **FastAPI:** JSON API with OpenAPI docs.
- **Power BI report:** Desktop-verified two-page project with six DAX measures and synthetic source rows.

## Architecture

See [docs/architecture.md](docs/architecture.md). At a glance:

```text
Opportunity scoring -> Triage API -> Rule baseline + lexical knowledge retrieval
                                      -> Draft + source references + fallback
                                      -> Human review + audit log
                                      -> Evaluation cases + Power BI-ready metrics
```

## File structure

```text
criticalops-ai-workbench/
├── app.py                          # Streamlit portfolio demo
├── api.py                          # FastAPI endpoints
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── core/
│   ├── __init__.py
│   ├── schemas.py                  # Request validation schemas
│   ├── scoring.py                  # Use-case scoring logic
│   ├── knowledge.py                # Local lexical retrieval baseline
│   ├── generation.py               # Optional grounded LLM adapter
│   ├── triage.py                   # Category, priority and response logic
│   ├── evaluation.py               # Synthetic evaluation runner
│   └── store.py                    # SQLite incident log and audit events
├── scripts_generate_powerbi.py    # Regenerate the synthetic Power BI CSV
├── data/
│   ├── knowledge/maintenance_sop.md # Fictional reference articles
│   └── demo/
│       ├── evaluation_cases.json   # Labelled synthetic evaluation cases
│       └── use_cases.json          # Use-case examples
├── docs/
│   ├── user_stories.md
│   ├── architecture.md
│   ├── business_case.md
│   ├── test_plan.md
│   └── risk_register.md
├── powerbi/
│   ├── sample_incidents.csv        # Synthetic dashboard dataset
│   └── model_and_measures.md       # Power BI model, visuals, DAX
└── tests/
    ├── test_scoring.py
    ├── test_triage.py
    └── test_evaluation.py
```

## Run locally

Use Python 3.10 or later.

### 1. Create the environment

```bash
python -m venv .venv
```

Activate it:

- Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Install packages:

```bash
python -m pip install -r requirements.txt
```

### 2. Start the user interface

```bash
streamlit run app.py
```

The app opens in your browser. The SQLite database is created in `data/workbench.sqlite` on first use. It is ignored by Git.

### 3. Start the API (separate terminal)

```bash
uvicorn api:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API testing. Health check: `http://127.0.0.1:8000/health`.

### 4. Run tests

```bash
pytest -q
```

## API quick reference

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health and demo mode |
| GET | `/api/use-cases` | List scored sample opportunities |
| POST | `/api/use-cases/score` | Score a proposed opportunity |
| POST | `/api/incidents/triage` | Triage and persist a synthetic incident |
| GET | `/api/incidents` | List incidents and review status |
| POST | `/api/incidents/{incident_id}/review` | Record a human review decision |
| POST | `/api/evaluate` | Run synthetic evaluation set |
| GET | `/api/metrics` | Summary metrics |
| GET | `/api/incidents/{incident_id}` | Incident detail and current version |
| GET | `/api/incidents/{incident_id}/audit` | Application audit history |

Example request:

```json
{
  "description": "Pump PUMP-204 has rising vibration and unusual bearing noise",
  "asset_id": "PUMP-204",
  "site": "Demo Manufacturing Site",
  "production_impact": 3,
  "estimated_downtime_hours": 1,
  "safety_related": false
}
```

## Evaluation honesty

The data set is synthetic and small. The evaluation metrics measure this test set only; they do not prove production accuracy, safety, savings or customer outcomes. The initial retrieval is keyword-based, not embeddings/vector search. The response generation is templated in offline mode. This is a conscious MVP boundary that provides a baseline before more complex LLM features are added.

## Important limitations

- No customer APIs, internal systems or private operational data are used.
- No physical equipment is controlled and no repair/stop/restart action is executed.
- Human review is a workflow feature, not a production identity/authorisation system.
- No vector database or external LLM is configured by default; the optional LLM adapter is still not an agent or a production integration.
- Deployment security, secrets management, tenancy, observability, and disaster recovery are not production-grade.

## Demonstration flow (5 minutes)

1. Explain the operational problem and the measurable hypothesis.
2. Score three use cases and explain why autonomous repair is not a safe first pilot.
3. Submit a pump vibration or sensor-quality incident.
4. Show the category, priority rationale, cited local article and fallback/human-review controls.
5. Record an approval or request-more-information outcome.
6. Run the evaluation suite and show a failure case.
7. Show the operational metrics/Power BI-ready data.
8. Explain how you would add semantic retrieval, approved connectors, identity, observability, model-cost logging and a controlled production pilot.

