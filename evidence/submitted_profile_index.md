# Submitted profile evidence index

Audit date: 30 October 2026. Reference: the candidate's submitted Atos AI Consultant resume. This index documents present evidence, not retrospective completion. Employer documents and the resume itself are not published here.

| Resume claim | Evidence and reproduction | Status / limitation |
|---|---|---|
| Assessed value, feasibility, data readiness, cost and risk | [Business case](../docs/business_case.md), [scoring](../core/scoring.py), [workflow](../docs/workflow.md), [stories](../docs/user_stories.md), [adoption guide](../docs/analyst_guide.md) | Demonstrated prototype analysis; costs and benefits are hypotheses |
| FastAPI triage, references, fallback, versioned review and audit | [API](../api.py), [core](../core), [tests](../tests); run `pytest -q` | 23 tests passed again on audit date; reviewer labels are not authenticated identities |
| 13 baseline and 36 challenge cases | [Results](README.md); run `python scripts/evaluate.py` | Synthetic, developer-authored; not independent production validation |
| Two-page report and six DAX measures | [Desktop verification](powerbi_verification.md), [project](../powerbi/desktop); open PBIP, refresh, inspect filters and reopen | Recorded native verification; no service publication or measured savings |
| OpenAPI 2.0 connector | [Connector](../connectors), [contract tests](../tests/test_connector.py) | Locally validated only; import and live execution unverified |
| Copilot Studio tested on same 13 cases | [Current status](../integrations/copilot/STATUS.md) | Unresolved: 12 prepared acceptance tests have blank results; Python tests do not establish agent performance |
| Copilot Chat drafting and corrections | No captured product session | Unresolved; retain actual prompts, outputs, corrections and source checks from future exercise |
| Power Apps and Power Automate | No verified product implementation | Unresolved; requires actual app and flow runs, including rejection and failures |
| Microsoft Applied Skills assessments passed | Requires Microsoft Learn issuer verification links | Unresolved; repository work cannot establish credentials |
| Anthropic courses and other credentials | Requires issuer records | Candidate reported; not authenticated by this repository |
| Employer kiosk hybrid retrieval and routing | Requires approved employer implementation evidence | Separate from this keyword-based project; no implied validation |
| Registration portal on EC2, proposals and events | Requires permitted employer records | Separate historical claims; a new demo cannot authenticate them |
| PRI career analysis | [Repository](https://github.com/codervelavan/pri-platform) | Inspected snapshot contains relevant implementation; README describes older prompt-scoring features; current execution still required |
| PowerPredictor synthetic dashboard | [Repository](https://github.com/codervelavan/MSME-Early-Warning-System) | Inspected notebook includes 2,880 synthetic rows across 80 enterprises; README and reproducible dashboard need work |

## Outstanding verification sequence

1. Run 13 baseline scenarios against the actual unpublished Copilot agent, separately from the existing 12 acceptance cases. Capture responses, supporting source, fallback/escalation outcome, date and agent configuration. Keep failures.
2. Capture one Copilot Chat user-story draft and one SOP summary, with corrections justified against synthetic source material.
3. Build a synthetic reviewer app and approval flow. Verify approve, reject, timeout/error, duplicate trigger, permissions and stale-version conflict.
4. Import the connector only with an approved reachable authenticated API. Do not expose this local unauthenticated prototype.
5. Verify PRI from a current checkout and repair its README; make PowerPredictor executable from documented dependencies.
6. Add issuer credential links only when available. Record employer evidence privately unless publication is explicitly permitted.

Every new result must carry its actual execution date and configuration. Missing product access remains a dependency, never a passing result.
