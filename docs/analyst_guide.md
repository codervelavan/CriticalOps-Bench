# Analyst demonstration guide

Use this local prototype to inspect evidence-linked recommendations and review decisions. Use synthetic tickets only. It is not an equipment operating procedure or a production application.

## Use the workbench

1. Start the API or Streamlit using the README commands; keep services bound to localhost.
2. Assess a use case using the readiness rubric. Scores support discussion rather than establish ROI.
3. Submit a fictional incident with a unique ID, symptoms, impact and safety flag.
4. Inspect category, proposed priority, source references and uncertainty. Open the fictional SOP and verify support.
5. If evidence is insufficient, request details or escalate. Safety concerns require qualified review; never execute physical actions from a generated response.
6. Approve, reject or request information with a note. Reviewer names are unverified labels.
7. A stale review produces a conflict. Reload and inspect the latest state. Approved/rejected records are final in this prototype.
8. Inspect incident detail and audit-history API responses. SQLite records are editable application history, not immutable compliance logs.

## Five minute demonstration

- Minute 1: explain the hypothetical problem and proposed quality/time measures.
- Minute 2: show the rubric, user story and acceptance criteria.
- Minute 3: show a supported ticket, an unsupported question and a safety case.
- Minute 4: review an incident and demonstrate a duplicate or stale update conflict.
- Minute 5: explain evaluation failures and reporting verification status. Distinguish software tests, synthetic evaluation and unmeasured business value.

## Adoption and permissions

A real pilot needs approved sources, trained reviewers, authentication, source permissions, retention rules and a process owner. A reviewer-name field does not establish these controls. Explain limitations and capture feedback before rollout.
