# Figures

This folder contains selected report-ready PNG figures generated from aggregate validation and BI outputs.

Current figures:

- `post_discharge_utilization_dashboard_final.png`
- `sensitivity_interpretation_dashboard.png`
- `workflow_architecture.png`
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

The final dashboard, sensitivity interpretation, and workflow architecture images are the primary portfolio visuals used in the root README, final report, and Gradio app:

- `post_discharge_utilization_dashboard_final.png` summarizes the cohort, readmission outcome, post-discharge utilization, outpatient follow-up timing, and prior utilization signal.
- `sensitivity_interpretation_dashboard.png` summarizes prior utilization stratification, prior ED use stratification, follow-up window sensitivity, and model sensitivity interpretation.
- `workflow_architecture.png` documents the validation-first SQL/Python workflow from raw local Synthea CSVs through analysis and communication outputs.

The older generated figures remain available as supporting report assets and can be regenerated from aggregate outputs when applicable.

These figures are based on synthetic aggregate outputs only. They do not contain real patient data or patient-level synthetic records.
