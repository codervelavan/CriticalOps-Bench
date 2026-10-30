# Power BI Desktop verification

Verified on 30 October 2026 in Desktop 2.159.883.0, using the portable project at `powerbi/desktop/CriticalOps.pbip`.

| Check | Observed result |
|---|---|
| Refresh | Power Query executed the embedded synthetic CSV import; 13 rows loaded. |
| Baseline DAX/report values | Cases 13; category match 92.3%; priority match 100.0%; safety routing 100.0%; fallback 7.7%; mismatches 1. |
| Native DAX engine | An All-versus-Mismatch query executed successfully against the original model. Report cards subsequently reconciled the final model after the COALESCE changes. |
| Page rendering | Synthetic Evaluation and Case Review both rendered. |
| Mismatch filter | EVAL-013 only, expected leak_or_pressure versus predicted general_maintenance. |
| Fallback filter | EVAL-009 only. |
| Critical-review filter | EVAL-002, EVAL-003, EVAL-007, EVAL-010. |
| Reset | All 13 rows visible again; overview restored. |
| Persistence | Native save completed; report closed and reopened from the saved PBIP with the same baseline values. |

Screenshots: [overview](screenshots/powerbi_overview.png), [mismatch](screenshots/powerbi_mismatch_filter.png), [fallback](screenshots/powerbi_fallback_filter.png), [priority](screenshots/powerbi_priority_filter.png), [reopened](screenshots/powerbi_reopened.png).

All data is synthetic. The report describes agreement with author-written labels, not production accuracy or measured business value. It has no human time baseline, no realised savings measure and no Service publication. Prepared report sources are portable; first use on another computer requires Refresh because local caches are intentionally excluded.

Reproduction: open the PBIP, Refresh, compare the six cards, use Case Review slicers, clear each selection, save and reopen. Explain the safety denominator (four cases), separate priority/category agreement, and discuss the known failure. Review the Power Query steps and six DAX definitions before demonstrating the report in an interview.
