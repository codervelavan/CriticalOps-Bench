# Business case: CriticalOps AI Workbench

## Executive summary

Maintenance analysts may spend time classifying equipment incidents, locating approved procedures, asking for missing information and routing tickets. A grounded decision-support assistant could help standardise triage and reduce search effort, while qualified staff retain decision authority.

This portfolio case demonstrates the *method* for evaluating such a use case. It does not assert that a customer has this baseline or that this prototype saves a specific amount of time.

## Business problem hypothesis

- Ticket descriptions may be inconsistent and incomplete.
- Relevant procedures may live across documents or knowledge systems.
- Urgency and team routing may depend on process knowledge.
- A generic AI answer without source evidence may increase rather than reduce operational risk.

These points are hypotheses to validate with stakeholders and sample data, not verified facts about a particular company.

## Proposed minimum viable pilot

1. Select one non-safety-critical incident category with a clear baseline.
2. Use approved, versioned SOP articles and a labelled historical ticket sample.
3. Build a triage and retrieval assistant that returns evidence, missing details and uncertainty.
4. Keep all suggested changes and operational decisions subject to an authorised human.
5. Compare the assistant with the current manual process using a pre-agreed evaluation set.
6. Expand only if quality, security, adoption and economics meet stakeholder criteria.

## Value equation

Illustrative monthly time saved (hours) = eligible tickets per month × measured average minutes saved per ticket ÷ 60.

Illustrative gross labour value = hours saved × agreed fully loaded labour cost per hour.

Net monthly value = gross labour value − incremental monthly model, platform, integration, review and support costs.

Do not use these formulas to claim savings before measuring the ticket baseline, a representative pilot and review burden. Avoid counting time saved as cash savings unless budgets or staffing actually change.

## Proposed success measures

- Category accuracy on a holdout set.
- Priority agreement, reported separately from category accuracy.
- Retrieval relevance / evidence-support pass rate.
- Unsupported-answer fallback rate.
- Human edit, reject and escalation rates.
- Median handling time in baseline vs pilot.
- Cost per processed ticket, including human review and model usage.
- Adoption and repeat use among eligible analysts.
- Safety-escalation recall on a separately designed safety test set.

## Decision gates

- **Gate 1 — Discovery:** stakeholders agree on problem, baseline, source ownership, user group and exclusions.
- **Gate 2 — Prototype:** assistant passes predefined functional, grounding and fallback tests.
- **Gate 3 — Controlled pilot:** security and access controls are reviewed; human oversight is staffed; baseline is measured.
- **Gate 4 — Scale decision:** value, risk, user feedback and operating cost meet agreed thresholds.
