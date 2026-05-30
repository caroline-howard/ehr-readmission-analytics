# Reproducibility Guide

This guide explains how to reproduce the synthetic EHR readmission analytics workflow from local Synthea CSV files. The repository does not include raw patient-level CSVs or processed databases.

## 1. Install Requirements

From the repository root:

```bash
python -m pip install -r requirements.txt
```

The project uses Python, pandas, DuckDB, Jupyter, statsmodels, matplotlib, and Gradio.

## 2. Add Local Synthea Data

Place Synthea synthetic CSV exports in:

```text
data/raw/
```

Core files used by the current cohort workflow:

- `patients.csv`
- `encounters.csv`
- `conditions.csv`

Additional files may be present for profiling or future exploratory work:

- `observations.csv`
- `medications.csv`
- `payers.csv`
- `payer_transitions.csv`

Raw files are ignored by git and should not be committed.

## 3. Run Source Data Profiling

Use either the notebook or command-line profiling script:

```bash
jupyter notebook notebooks/01_synthea_data_profile.ipynb
```

or:

```bash
python scripts/profile_synthea_data.py
```

Profiling confirms available tables, table shapes, column names, encounter class values, date fields, and missingness before cohort SQL is run.

## 4. Run SQL Workflow

The SQL scripts are DuckDB-compatible and should be run from the repository root.

Example:

```bash
duckdb data/processed/ehr_readmission.duckdb < sql/01_profile_source_tables.sql
duckdb data/processed/ehr_readmission.duckdb < sql/02_define_eligible_inpatient_encounters.sql
duckdb data/processed/ehr_readmission.duckdb < sql/03_define_index_encounter.sql
duckdb data/processed/ehr_readmission.duckdb < sql/04_define_postdischarge_utilization.sql
duckdb data/processed/ehr_readmission.duckdb < sql/05_define_30_day_readmission.sql
duckdb data/processed/ehr_readmission.duckdb < sql/06_create_final_analysis_dataset.sql
duckdb data/processed/ehr_readmission.duckdb < sql/07_create_validation_outputs.sql
duckdb data/processed/ehr_readmission.duckdb < sql/08_create_bi_dashboard_tables.sql
```

This creates or refreshes:

- cohort construction views
- validation QA outputs in `outputs/validation/`
- dashboard-ready aggregate tables in `outputs/bi/`

Processed DuckDB databases are ignored by git.

## 5. Run Analysis Notebooks

Run the descriptive and modeling notebooks after SQL outputs have been reviewed:

```bash
jupyter notebook notebooks/02_descriptive_analysis.ipynb
jupyter notebook notebooks/03_logistic_regression.ipynb
```

These notebooks regenerate:

- `outputs/analysis/table1_baseline_characteristics.csv`
- `outputs/analysis/readmission_summary.csv`
- `outputs/analysis/outpatient_followup_summary.csv`
- `outputs/analysis/ed_revisit_summary.csv`
- `outputs/analysis/logistic_regression_results.csv`
- `outputs/analysis/logistic_regression_model_notes.csv`
- `outputs/figures/logistic_regression_odds_ratios.png`

The notebooks use patient-level synthetic records only in local memory and export aggregate summaries or model coefficients only.

## 6. Regenerate Figures

Report figures are generated from aggregate outputs and stored in:

```text
outputs/figures/
```

Current figures include cohort attrition, post-discharge KPIs, encounter class distribution, the logistic regression odds ratio plot, and a dashboard mockup.

## 7. Run the Gradio Demo

After aggregate outputs exist, run:

```bash
python app/app.py
```

The app displays aggregate KPI cards, figures, dashboard-ready tables, Table 1 outputs, exploratory logistic regression results, and report links.

## Data Governance Notes

- Do not commit raw Synthea CSV files.
- Do not commit processed databases or patient-level extracts.
- Do not add real patient data.
- Committed outputs should remain aggregate, small, and reproducible.
- Synthetic-data results should not be interpreted as clinical evidence or used for decision-making.
