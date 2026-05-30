# Notebooks

This folder contains notebook-based workflow steps for the synthetic EHR readmission analytics project.

Current notebook:

- `01_synthea_data_profile.ipynb` profiles local Synthea CSV extracts before cohort SQL is written or refreshed.

The profiling notebook checks available files, table shapes, columns, encounter classes, date fields, and missingness. It reuses the command-line profiling logic in `scripts/profile_synthea_data.py` so notebook and script behavior stay aligned.

Future notebooks may cover descriptive summaries, statistical analysis, and report-ready figures after the SQL cohort and validation workflow has been reviewed.

Notebook outputs should stay lightweight, reproducible, and free of real patient data.
