# Capability evidence index

Verified scope as of 30 October 2026.

| Capability | Evidence | Boundary |
|---|---|---|
| Use-case assessment | [Business case](../docs/business_case.md), [workflow](../docs/workflow.md), [stories](../docs/user_stories.md) | Proposed value, not measured savings |
| Triage and review | [API](../api.py), [tests](../tests) | Local prototype; reviewer labels are not authenticated identities |
| Evaluation | [Results](README.md) | 13 baseline and 36 synthetic challenge cases; no production validation |
| Reporting | [Desktop verification](powerbi_verification.md) | Two pages, six measures; no service publication |
| Connector | [Definition and instructions](../connectors/README.md) | Locally validated, not live integration |
| Copilot Studio | [Status](../integrations/copilot/STATUS.md) | Prepared tests remain unexecuted against an accessible agent |
| Power Apps and Power Automate | No verified product execution | Pending environment access and implementation |

Run `pytest -q` and `python scripts/evaluate.py` to reproduce the Python checks. Follow the Desktop verification instructions for reporting. New product results must include actual execution dates, configuration and failures. No credentials, employment history or customer adoption are established by this repository.

Run `python scripts/demo_review.py` for a seven-step synthetic review demonstration. The [recorded transcript](local_review_demo.json) includes real local API responses, duplicate and stale-review conflicts, final approval and audit history. It uses a temporary database and disables the optional external model. It is not a Power Automate or Copilot Studio execution trace.
