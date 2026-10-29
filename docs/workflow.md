# Maintenance analyst workflow

All incidents and procedures are fictional. The baseline is a workflow hypothesis, not an observed customer process.

## As is hypothesis

```mermaid
flowchart LR
    A[Receive incident] --> B[Clarify symptoms and impact]
    B --> C[Search approved procedures manually]
    C --> D[Select queue and proposed priority]
    D --> E[Qualified reviewer decides]
```

## Prototype workflow

```mermaid
flowchart LR
    A[Synthetic incident] --> B[Rules suggest category and priority]
    B --> C[Keyword retrieval returns references]
    C --> D{Evidence sufficient?}
    D -->|No| E[Fallback and request information]
    D -->|Yes| F[Evidence linked draft]
    E --> G[Human review]
    F --> G
    G --> H[Approve reject or request information]
    H --> I[Versioned record and application audit history]
```

Safety-related incidents bypass model drafting. No machine action is executed. Record versions prevent stale updates; final approvals/rejections cannot be silently replaced.

## Proposed pilot

Agree scope, approved sources, historical cases and quality thresholds with stakeholders. Measure manual versus assisted lookup time and correct-source selection on comparable tasks. Track corrections, fallback, escalation, adoption and operating cost. No human productivity benchmark or customer outcome has been measured.
