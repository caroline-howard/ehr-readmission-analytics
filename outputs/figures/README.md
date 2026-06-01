# Figures

This folder contains selected report-ready PNG figures used in the README, final report, and portfolio demo app. Figures are based on aggregate synthetic-data outputs only.

Current figures:

- `dashboard_mockup_professional.png` - approved dashboard mockup used in the README, report, and app
- `cohort_attrition_flow.png`
- `cumulative_outpatient_followup_curve.png`
- `readmission_by_prior_utilization_group.png`
- `logistic_regression_forest_plot_professional.png`
- `cohort_attrition.png`
- `postdischarge_kpis.png`
- `encounter_class_distribution.png`
- `logistic_regression_odds_ratios.png`

The professional figures can be refreshed with:

```bash
python scripts/generate_professional_figures.py
```

The dashboard mockup is preserved when the figure-generation script is rerun so the approved visual does not get overwritten. These figures do not contain real patient data or patient-level synthetic records.
