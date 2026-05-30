# Outputs

This folder contains selected aggregate project artifacts generated from the synthetic EHR workflow.

Most generated files are ignored by default to avoid committing large artifacts, raw data extracts, local databases, or premature analysis results. Profiling outputs such as `data_profile_summary.csv` are reproducible from local runs of the notebook or command-line profiling script and should not be committed unless intentionally included as a small portfolio artifact.

Currently committed output folders:

- `outputs/validation/` contains aggregate QA tables for cohort attrition, index encounter checks, date validity, encounter classes, missingness, readmission timing, and outpatient follow-up timing.
- `outputs/bi/` contains Power BI/Tableau-ready aggregate tables for cohort summary, readmission KPIs, follow-up timing, ED revisits, and demographic/utilization summaries.

These committed outputs do not contain real patient data or patient-level synthetic records. Raw Synthea CSV files remain outside version control in `data/raw/`. Processed data and local database files remain outside version control in `data/processed/`.
