# SQL

This folder contains DuckDB-compatible SQL scripts for the Week 2 cohort construction milestone. The scripts assume Synthea CSV files are stored locally in `data/raw/` and run from the repository root.

Run order:

1. `01_profile_source_tables.sql`
2. `02_define_eligible_inpatient_encounters.sql`
3. `03_define_index_encounter.sql`
4. `04_define_postdischarge_utilization.sql`
5. `05_define_30_day_readmission.sql`
6. `06_create_final_analysis_dataset.sql`
7. `07_create_validation_outputs.sql`

Example:

```bash
duckdb data/processed/ehr_readmission.duckdb < sql/01_profile_source_tables.sql
duckdb data/processed/ehr_readmission.duckdb < sql/02_define_eligible_inpatient_encounters.sql
duckdb data/processed/ehr_readmission.duckdb < sql/03_define_index_encounter.sql
duckdb data/processed/ehr_readmission.duckdb < sql/04_define_postdischarge_utilization.sql
duckdb data/processed/ehr_readmission.duckdb < sql/05_define_30_day_readmission.sql
duckdb data/processed/ehr_readmission.duckdb < sql/06_create_final_analysis_dataset.sql
duckdb data/processed/ehr_readmission.duckdb < sql/07_create_validation_outputs.sql
```

The scripts create reusable views for:

- source table profiling
- eligible adult inpatient encounters
- first eligible index hospitalization
- post-discharge outpatient follow-up and ED revisit measures
- all-cause 30-day inpatient readmission
- final MVP analysis dataset
- aggregate validation outputs for cohort attrition, index encounter checks, date validity, encounter classes, missingness, readmission timing, and outpatient follow-up timing

Generated databases and source CSVs are not stored here. Small aggregate QA tables may be intentionally committed under `outputs/validation/`.
