# Analysis Outputs

This folder contains intentionally committed aggregate analysis outputs generated from the notebook workflow.

Current outputs:

- `table1_baseline_characteristics.csv`
- `readmission_summary.csv`
- `outpatient_followup_summary.csv`
- `ed_revisit_summary.csv`
- `risk_stratification_summary.csv`
- `prior_utilization_group_summary.csv`
- `prior_utilization_stratification.csv`
- `prior_ed_use_stratification.csv`
- `followup_window_sensitivity.csv`
- `model_comparison_sensitivity.csv`
- `model_without_followup_results.csv`
- `model_with_followup_results.csv`
- `logistic_regression_results.csv`
- `logistic_regression_model_notes.csv`

The risk stratification summary is intended to support healthcare analytics interpretation by showing readmission and utilization patterns across selected age, chronic condition burden, and sex groups. Small strata and low event counts should not be overinterpreted.

The prior utilization stratification and prior ED use outputs support a more operational dashboard story around utilization burden before index hospitalization. These files summarize readmission, follow-up, and ED revisit rates across practical stakeholder-facing groups.

The follow-up window sensitivity and model comparison outputs document how observed follow-up patterns and adjusted models change when 7-day, 14-day, and 30-day follow-up variables are considered. These outputs are descriptive and timing-aware; they should not be interpreted as causal evidence.

These files are based on Synthea synthetic data and contain aggregate summaries or model coefficients only. They do not include real patient data or patient-level synthetic records.
