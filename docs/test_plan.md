# Evaluation and test plan

## What is implemented

- Unit tests for the use-case scoring rubric.
- Unit tests for category and safety-priority rules.
- Synthetic labelled evaluation cases in `data/demo/evaluation_cases.json`.
- A test runner that reports exact-match category/priority rates and whether safety-marked cases are routed to human review.

## What the evaluation does not prove

The evaluation cases are synthetic and small. An exact-match percentage only describes this defined test set. The test suite also exercises API triage and review persistence. It does not establish production readiness, generalisation to real tickets, safety certification, or business impact. Human reviewers should inspect false positives and false negatives rather than relying on one aggregate score.

## Recommended additional tests before production

1. Separate training/development and holdout test cases by incident source/time to prevent leakage.
2. Test paraphrases, spelling errors, abbreviated asset names, multilingual tickets, and missing context.
3. Test prompt injection in ticket text and knowledge articles.
4. Verify that evidence references match the actual retrieved document versions.
5. Add access-control tests proving users cannot retrieve articles they are not authorised to see.
6. Test model timeouts, invalid JSON, empty retrieval, stale articles, duplicate events and rate limits.
7. Run a safety-focused test suite with domain experts and approved site policy; do not rely on keyword checks alone.
8. Compare human-only, rules-only and AI-assisted workflows on the same representative cases.
