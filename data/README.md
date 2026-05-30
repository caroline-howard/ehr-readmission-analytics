# Data

This project uses Synthea synthetic EHR CSV files for local development. The `data/raw/` and `data/processed/` folders are intentionally empty on GitHub except for `.gitkeep` files.

Keeping these folders empty in version control is deliberate:

- raw Synthea CSVs can be large
- processed DuckDB, SQLite, Parquet, or CSV files are reproducible
- public portfolio repositories should avoid committing patient-level data artifacts, even when the data are synthetic
- the committed outputs in this project are limited to small aggregate QA and BI tables

## Local Raw Data Setup

Place local Synthea CSV exports in `data/raw/`.

Common source files expected by the profiling and SQL workflow include:

- `patients.csv`
- `encounters.csv`
- `conditions.csv`
- `observations.csv`
- `medications.csv`
- `payers.csv`
- `payer_transitions.csv`

The core cohort SQL currently depends on `patients.csv`, `encounters.csv`, and `conditions.csv`. Other Synthea files may support later exploratory variables but are not required for the current MVP cohort build.

## Local Processed Data

Use `data/processed/` for local generated databases or analysis-ready files, such as:

- DuckDB databases
- SQLite databases
- processed CSV extracts
- Parquet files

These files are ignored by git and should not be committed. They can be recreated by running the SQL workflow.

## Recommended Workflow

1. Add Synthea CSV files locally to `data/raw/`.
2. Run the profiling workflow:
   - `notebooks/01_synthea_data_profile.ipynb`
   - or `scripts/profile_synthea_data.py`
3. Run the SQL scripts in `sql/` to build cohort, validation, and BI aggregate outputs.
4. Review committed aggregate outputs in:
   - `outputs/validation/`
   - `outputs/bi/`

No real patient data should be added to this repository.
