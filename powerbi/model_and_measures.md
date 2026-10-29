# Power BI handoff

## Quick start

1. Open Power BI Desktop.
2. Select **Get data → Text/CSV** and import `powerbi/sample_incidents.csv`.
3. Confirm `created_date` is a date, booleans are true/false, and numeric fields are numeric.
4. Create cards for total incidents, category exact-match rate, priority exact-match rate and safety escalation pass rate.
5. Add a category bar chart, date trend, priority distribution and a table of failures.
6. Add slicers for category, site, priority and evaluation outcome.
7. Keep synthetic data clearly labelled on the report page.

## Suggested visuals

- KPI cards: total synthetic tickets, category exact match, priority exact match, safety-routing checks.
- Bar chart: ticket count by category and suggested priority.
- Trend: number of synthetic incidents by date.
- Matrix: expected vs predicted category.
- Table: cases with category/priority mismatch and fallback status.

## Example DAX

```DAX
Total Incidents = COUNTROWS(SampleIncidents)

Category Exact Matches =
CALCULATE(
    COUNTROWS(SampleIncidents),
    SampleIncidents[category_pass] = TRUE()
)

Category Exact Match % =
DIVIDE([Category Exact Matches], [Total Incidents], 0)

Priority Exact Matches =
CALCULATE(
    COUNTROWS(SampleIncidents),
    SampleIncidents[priority_pass] = TRUE()
)

Priority Exact Match % =
DIVIDE([Priority Exact Matches], [Total Incidents], 0)

Safety Escalation Pass % =
DIVIDE(
    CALCULATE(
        COUNTROWS(SampleIncidents),
        SampleIncidents[safety_expected] = TRUE(),
        SampleIncidents[safety_escalation_pass] = TRUE()
    ),
    CALCULATE(COUNTROWS(SampleIncidents), SampleIncidents[safety_expected] = TRUE()),
    0
)
```

Format rate measures as percentages. These measures summarise only the synthetic dataset, not production quality or business impact.
