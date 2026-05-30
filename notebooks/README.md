# Notebooks

This folder contains notebook-based workflow steps for the synthetic EHR readmission analytics project.

Current notebook:

- `01_synthea_data_profile.ipynb` profiles local Synthea CSV extracts before cohort SQL is written or refreshed.
- `02_descriptive_analysis.ipynb` generates Table 1, readmission summary, outpatient follow-up summary, and ED revisit summary outputs.
- `03_logistic_regression.ipynb` fits an exploratory logistic regression model for 30-day inpatient readmission and exports model coefficients plus an odds ratio plot.

The profiling notebook checks available files, table shapes, columns, encounter classes, date fields, and missingness. It reuses the command-line profiling logic in `scripts/profile_synthea_data.py` so notebook and script behavior stay aligned.

The analysis notebooks rebuild the final analysis dataset from the SQL workflow, use patient-level synthetic records only in local memory, and export aggregate tables or model coefficients only.

Notebook outputs should stay lightweight, reproducible, and free of real patient data.
