# Learn the project through a five-minute demonstration

1. Explain the hypothesis: analysts need to classify incidents and find approved guidance. No customer time saving has been measured.
2. Submit a synthetic pump-vibration incident. Trace request validation, rule-based category/priority, keyword overlap retrieval and source references. Default responses are templated; the optional LLM is disabled in evaluation.
3. Show an unsupported query and a safety case. Explain fallback and qualified human review. A relevant source does not guarantee a correct generated answer.
4. Review an incident, then show duplicate-ID or stale-version rejection and audit history. Explain why application history is not immutable compliance evidence.
5. Open the Power BI report. Explain 13 baseline rows, category versus priority agreement, the four-case safety denominator, fallback and mismatch filters. Discuss a failed case.

## Microsoft contribution

Power BI is the verified reporting layer. Power Query prepares rows; DAX measures calculate values in the current filter context. Copilot Studio would supply the conversational interface, Power Automate the approval routing, Power Apps the reviewer screen, and a custom connector the API bridge. These latter integrations require separate live verification; the repository definition alone is insufficient.

## Next learning milestones

- Explain a user story, acceptance criterion and proposed business measure without reading notes.
- Demonstrate the existing system yourself and explain its failure cases.
- Complete the actual Microsoft review workflow using synthetic records and capture successful and failed runs.
- Compare keyword retrieval with hybrid retrieval and reranking on a separately labelled frozen test set; preserve the original baseline.
- Run a consented, counterbalanced manual-versus-assisted lookup exercise. Report correctness and review burden alongside elapsed time; do not generalise a small usability exercise into customer ROI.

The next build is a complete analyst-review workflow, not another disconnected chatbot. Choose tools based on the user's workflow, access constraints, operating costs and measurable usefulness.
