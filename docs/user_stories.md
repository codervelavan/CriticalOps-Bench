# User stories and acceptance criteria

## Product objective

Help an enterprise AI consultant assess an operational AI opportunity, demonstrate a safe prototype, record evidence from testing, and communicate measured value. The factory-maintenance scenario is fictional and all ticket data is synthetic.

## Primary user story

**As a maintenance operations analyst, I want to receive an evidence-linked triage recommendation for an equipment incident so that I can route work consistently, find relevant approved guidance faster, and keep a qualified human responsible for the final decision.**

### Acceptance criteria

1. Given a ticket with a description, asset ID and impact, the system returns a suggested category, priority rationale and owning queue.
2. The system retrieves and names zero or more relevant demo knowledge articles.
3. When useful evidence is not retrieved, it explicitly says evidence is insufficient and recommends human escalation rather than fabricating instructions.
4. A reported safety concern is routed to critical human review.
5. The output clearly marks itself as a suggestion; no machine command, repair action or physical action is executed.
6. The incident and generated recommendation are recorded locally.
7. A reviewer can approve, reject or request more information and leave an audit note.
8. Tests compare the prediction with labelled synthetic cases and preserve failure cases.

## Supporting user stories

### US-02: AI consultant prioritises opportunities

As an AI consultant, I want a transparent, repeatable use-case scoring rubric so that I can compare potential AI use cases before recommending a pilot.

Acceptance: the score reflects business value, feasibility, data readiness, governance readiness, scalability and implementation effort; low readiness creates specific follow-up actions; the rubric is labelled as a discovery aid rather than a final business case.

### US-03: Maintenance lead sees operational trends

As a maintenance lead, I want to view category mix, pending reviews, fallback rate and evaluation outcomes so that I can spot workflow issues and decide where to improve the prototype.

Acceptance: dashboard fields have definitions; sample data is marked synthetic; measures can be independently checked against source rows.

### US-04: AI governance reviewer checks controls

As an AI governance reviewer, I want to see evidence sources, fallback decisions, human approval and review notes so that I can inspect how a recommendation was produced and what happened next.

Acceptance: source references and review status are visible; sensitive or uncertain cases are not silently auto-approved; review decisions have timestamps and actor labels.

### US-05: Developer integrates the prototype

As a developer, I want documented API endpoints and structured JSON schemas so that a UI or a future ticketing connector can integrate with the triage service.

Acceptance: OpenAPI docs are available at `/docs`; malformed input is rejected; health, scoring, triage, review, evaluation and metrics endpoints are documented.

## Out of scope

- Actual integration with Atos internal systems or any customer service-management platform.
- Real industrial telemetry ingestion or machine control.
- Automated safety decisions, lockout/tagout instructions, repairs, or equipment restarts.
- Production-grade identity, tenant isolation, key management, disaster recovery or regulatory certification.
- Claims of measured savings or production accuracy based on synthetic data.
