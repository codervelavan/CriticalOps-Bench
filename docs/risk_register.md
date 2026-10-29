# Risk register

| Risk | Why it matters | Demo control | Production treatment |
|---|---|---|---|
| Hallucinated or unsupported advice | Could lead to incorrect operational decisions | Local approved-demo SOPs, cited source IDs, explicit fallback | Validated retrieval, groundedness tests, human review, incident process |
| Unsafe physical action | Industrial interventions can be hazardous | No machine-control endpoint; all outputs are suggestions | Domain hazard analysis, safety engineering, formal authorisation and interlocks |
| Misclassification / wrong priority | Work may be routed incorrectly | Labelled synthetic tests and transparent rules | Representative holdout data, error-cost analysis, monitoring and override |
| Sensitive data exposure | Tickets may contain personal or operational secrets | Synthetic data only | Data minimisation, data classification, access policy, contractual and privacy review |
| Stale or incorrect SOP | Retrieval may select an outdated instruction | Fictional, versionable articles | Source ownership, version control, expiration, lineage and approved publishing |
| Prompt injection | Untrusted ticket text may try to manipulate the assistant | The baseline does not execute tools | Separate instructions from data, sanitisation, tool allowlists and adversarial tests |
| Excessive autonomy | An agent could perform a state-changing action | No automatic execution; review required | Explicit permitted actions, human gates, identity and auditable policy enforcement |
| Hidden costs / latency | AI costs can erode business value | Current baseline uses no external LLM | Log model, tokens, latency, retries, review effort and cost per task |
| Misleading success claims | Synthetic data can look more convincing than it is | Results are clearly labelled synthetic | Real baseline, pilot design, confidence intervals and honest reporting |
