# Figures

This folder contains selected report-ready PNG figures generated from aggregate validation and BI outputs.

Current figures:

- `post_discharge_utilization_summary_visual.png`
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

The post-discharge utilization summary visual is the main multi-panel figure used in the root README, final report, and Gradio app. It explains the current portfolio workflow across panels A-F: cohort attrition, readmission timing, utilization KPIs, age-group readmission rates, outpatient follow-up timing, and prior utilization comparison.

These figures are based on synthetic aggregate outputs only. They do not contain real patient data or patient-level synthetic records.
