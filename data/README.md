# Data

This project uses Synthea synthetic EHR CSV files for local development and portfolio demonstration.

Place raw Synthea CSV exports in `data/raw/`. Common files may include:

- `patients.csv`
- `encounters.csv`
- `conditions.csv`
- `observations.csv`
- `medications.csv`
- `payers.csv`
- `payer_transitions.csv`

Raw and processed data files are intentionally excluded from version control. This keeps the repository lightweight and prevents accidental commits of large files or data artifacts.

Use `notebooks/01_synthea_data_profile.ipynb` or `scripts/profile_synthea_data.py` to inspect available tables before writing final cohort SQL.

No real patient data should be added to this repository.
