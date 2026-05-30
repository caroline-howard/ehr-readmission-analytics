# SQL

This folder contains DuckDB-compatible SQL scripts for the Week 2 cohort construction milestone. The scripts assume Synthea CSV files are stored locally in `data/raw/` and run from the repository root.

Run order:

1. `01_profile_source_tables.sql`
2. `02_define_eligible_inpatient_encounters.sql`
3. `03_define_index_encounter.sql`
4. `04_define_postdischarge_utilization.sql`
5. `05_define_30_day_readmission.sql`
6. `06_create_final_analysis_dataset.sql`

Example:

```bash
duckdb data/processed/ehr_readmission.duckdb < sql/01_profile_source_tables.sql
duckdb data/processed/ehr_readmission.duckdb < sql/02_define_eligible_inpatient_encounters.sql
duckdb data/processed/ehr_readmission.duckdb < sql/03_define_index_encounter.sql
duckdb data/processed/ehr_readmission.duckdb < sql/04_define_postdischarge_utilization.sql
duckdb data/processed/ehr_readmission.duckdb < sql/05_define_30_day_readmission.sql
duckdb data/processed/ehr_readmission.duckdb < sql/06_create_final_analysis_dataset.sql
```

The scripts create reusable views for:

- source table profiling
- eligible adult inpatient encounters
- first eligible index hospitalization
- post-discharge outpatient follow-up and ED revisit measures
- all-cause 30-day inpatient readmission
- final MVP analysis dataset

Generated databases, source CSVs, and SQL outputs are not stored here.
