# CriticalOps Power BI project

This source project uses the public CriticalOps-Bench synthetic incident CSV. It contains two report pages, a Power Query import/cleaning pipeline, six DAX measures and a semantic model.

## Open and demonstrate

1. Extract the entire folder, keeping the Report and SemanticModel folders beside CriticalOps.pbip.
2. Open CriticalOps.pbip in a current Power BI Desktop version supporting PBIP/PBIR. Enable project/enhanced-report preview settings if your version requires them.
3. Refresh the model. The CSV is embedded in the Power Query partition as a portable snapshot; no service credentials or machine-specific paths are required.
4. Confirm 13 cases; category agreement 12/13 (92.3%); priority agreement 13/13; safety-routing checks 4/4; fallback rate 1/13 (7.7%); mismatch case EVAL-013.
5. Open Transform Data and explain CSV parsing, header promotion, boolean/date/number conversion, trimmed identifiers and the derived evaluation_result column.
6. Inspect the DAX measures. Explain why safety routing divides by four safety cases, not all thirteen rows, and why these figures do not measure real-world quality.
7. In Case Review, select Mismatch and inspect the expected vs predicted categories. Reset slicers to inspect all cases.
8. Save as a PBIX after checking rendering, filters and refresh. Add Power BI/Power Query/DAX to your resume only when you can demonstrate and explain this work yourself.

## Data interpretation

Every row is SYNTHETIC_DEMO. created_date values are generated labels, not a record of observed customer operations. review_status is synthetic_pending, not evidence of counsellor/engineer approvals. Downtime values are fictional inputs, not realised downtime reduction. Category and priority agreement are separate from safety routing. The dataset does not contain a manual baseline or measured task duration, so there is deliberately no time-savings KPI.

## Validation status

Verified in Microsoft Power BI Desktop 2.159.883.0 on 30 October 2026. The model refreshed successfully, both report pages rendered, and all six baseline measures matched the expected results. Mismatch filtering isolated EVAL-013; fallback=True isolated EVAL-009; critical_review isolated EVAL-002, EVAL-003, EVAL-007 and EVAL-010. Filters were reset. Native save completed, and the saved project was reopened with the same six baseline values.

The native check found that the report-definition metadata incorrectly used version 4.0.0. It was corrected to 2.0.0; the separate definition.pbir version remains 4.0. The model measures now use COALESCE for zero matching rows where appropriate. Power BI saved its normal .platform metadata. Local .pbi caches are excluded from source control and distribution.

See ../../evidence/screenshots/ and ../../evidence/powerbi_verification.md for the observed checks. Source-schema validation alone was not used to declare completion. No Power BI Service publication, automated refresh, customer deployment or measured time-savings KPI is claimed.

## Sources

- Dataset: https://github.com/codervelavan/CriticalOps-Bench/blob/main/powerbi/sample_incidents.csv
- Power BI project format: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
- Enhanced report format: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
- Semantic model format: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset
