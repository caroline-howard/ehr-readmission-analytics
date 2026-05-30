# BI Dashboard Tables

This folder contains intentionally committed aggregate CSV tables for a Power BI or Tableau dashboard layer. The tables are generated from Synthea synthetic data using the SQL workflow and are designed for portfolio demonstration of healthcare operations and population health reporting.

Included dashboard-ready tables:

- `cohort_summary_table.csv`
- `readmission_kpi_table.csv`
- `followup_timing_table.csv`
- `ed_revisit_table.csv`
- `demographic_utilization_summary_table.csv`

These files contain aggregate summaries only. They do not include real patient data or patient-level synthetic records, and they should not be interpreted as clinical results. They are reproducible by placing Synthea CSVs in `data/raw/` and running the SQL scripts in `sql/` in order, ending with `sql/08_create_bi_dashboard_tables.sql`.
