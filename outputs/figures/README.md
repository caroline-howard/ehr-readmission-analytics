# Figures

This folder contains selected report-ready PNG figures generated from aggregate validation and BI outputs.

Current figures:

- `dashboard_mockup_professional.png`
- `cohort_attrition_flow.png`
- `cumulative_outpatient_followup_curve.png`
- `readmission_by_prior_utilization_group.png`
- `logistic_regression_forest_plot_professional.png`
- `cohort_attrition.png`
- `postdischarge_kpis.png`
- `encounter_class_distribution.png`
- `logistic_regression_odds_ratios.png`
- `dashboard_mockup.png`

The professional figures can be regenerated with:

```bash
python scripts/generate_professional_figures.py
```

These figures are based on synthetic aggregate outputs only. They do not contain real patient data or patient-level synthetic records.
