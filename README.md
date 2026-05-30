# Retrospective Post-Discharge Utilization Analytics Workflow

[Overview](#project-overview) | [Research Question](#research-question) | [Workflow Design](#healthcare-analytics-workflow-design) | [Analytics Focus](#core-analytics-focus) | [Measures](#outcome-and-utilization-measures) | [Technical Environment](#technical-environment) | [Skills](#skills-demonstrated) | [Structure](#repository-structure) | [Data Setup](#data-setup) | [Outputs](#planned-outputs) | [Responsible Use](#responsible-use)

## Project Overview

This project demonstrates an end-to-end retrospective healthcare utilization analytics workflow using Synthea synthetic EHR data. It simulates a health system analytics request to define an adult inpatient cohort, track core post-discharge utilization measures, identify outpatient follow-up timing, and evaluate factors associated with 30-day inpatient readmission.

The project is built for healthcare analytics, clinical research analytics, and health system research data analyst roles where reproducibility, data governance, SQL logic, and clear communication are essential.

## Research Question

Among adult patients with a first eligible acute inpatient hospitalization in Synthea synthetic EHR data, how are outpatient follow-up timing, demographic characteristics, clinical conditions, prior utilization, and discharge-related factors associated with all-cause inpatient readmission within 30 days of discharge?

## What This Project Demonstrates

This project demonstrates the practical workflow behind a retrospective EHR analytics request: profiling raw data extracts, validating encounter classifications, defining an eligible inpatient cohort, deriving post-discharge utilization measures, creating a 30-day readmission outcome, and preparing reproducible analysis-ready outputs.

## Healthcare Analytics Workflow Design

This project follows a validation-first analytics workflow common in healthcare operations, population health, and clinical research analytics. Raw synthetic EHR extracts are profiled before cohort construction so available tables, fields, encounter classes, date structures, and missingness patterns are understood before outcome derivation.

The workflow emphasizes validation of encounter classification, temporal sequencing, missingness, and operational edge cases before analysis. SQL and Python are used to support reproducible, auditable healthcare analytics workflows that can be reviewed by technical analysts, clinical stakeholders, and population health teams.

This project intentionally separates data profiling, cohort construction, outcome derivation, validation, statistical analysis, and reporting so each step can be reviewed and updated independently.

## Why This Project Matters

Health system research and population health teams need reproducible workflows for defining cohorts, deriving post-discharge outcomes, validating EHR data, assessing missingness, conducting statistical analysis, and preparing manuscript-ready outputs. This project is intended to demonstrate those skills in a public, privacy-preserving way using synthetic data.

## Core Analytics Focus

- Retrospective EHR analytics
- Inpatient cohort construction
- Post-discharge utilization tracking
- 30-day readmission derivation
- Temporal sequencing validation
- SQL and Python healthcare analytics workflows
- Data validation and QA workflows
- Healthcare analytics-oriented documentation

## Outcome and Utilization Measures

- 30-day inpatient readmission
- ED revisit within 30 days
- Outpatient follow-up within 7, 14, and 30 days
- Days to first outpatient follow-up
- Total post-discharge encounters within 30 days

## Technical Environment

- SQL
- Python / pandas
- Jupyter notebooks
- Synthea synthetic EHR data
- Power BI or Tableau
- GitHub workflow with feature branching and pull requests

## Dashboard and BI Layer

The project also incorporates a healthcare operations and population health dashboard layer intended to simulate stakeholder-facing KPI reporting and utilization analytics workflows commonly used in health systems.

The BI layer is designed around readmission KPIs, follow-up analytics, ED revisit reporting, cohort summaries, and operational healthcare metrics. It is intended to support clear communication of cohort trends and post-discharge utilization patterns without presenting the project as a clinical decision tool.

## Analytic Scope

The project design is informed by health services research on outpatient follow-up and readmissions, including Balasubramanian et al. (2025), as well as published readmission studies and CMS readmission reporting examples. These sources motivate clear definitions for post-discharge time windows, outpatient follow-up exposure, inpatient readmission, ED revisits, mortality flags when available, comorbidity burden, age groups, disease groups, prior utilization, and baseline risk.

The first project version will focus on a core MVP variable set: patient demographics, index hospitalization dates, length of stay, prior utilization, outpatient follow-up within 7, 14, and 30 days, ED revisit within 30 days when identifiable, and 30-day inpatient readmission. Additional variables such as disease subgroups, discharge disposition, payer, mortality, post-acute setting, medication counts, and lab values will be treated as optional exploratory variables only if the Synthea export supports defensible derivation.

Planned validation checks include patient and encounter count reconciliation, duplicate review, encounter date ordering, length-of-stay plausibility, readmission window verification, follow-up timing verification, and assessment of missing or unexpected values in key analytic fields. Outpatient follow-up variables will be interpreted as observational utilization measures, not as evidence that follow-up causes readmission reduction.

## Skills Demonstrated

- Healthcare analytics
- Population health analytics
- Healthcare operations analytics
- Retrospective clinical research
- Synthetic EHR data
- SQL cohort definition
- 30-day readmission outcome derivation
- Post-discharge outpatient follow-up measures
- ED revisit utilization measures
- Data validation and QA
- Missingness assessment
- Logistic regression
- BI/dashboard reporting workflows
- Manuscript-style tables and figures
- Mock IRB/data governance documentation
- Hugging Face Gradio demo

## Planned Workflow

1. Project setup and documentation
2. Synthea data ingestion
3. SQL cohort definition
4. Post-discharge utilization measure derivation
5. 30-day readmission outcome derivation
6. Data validation and missingness assessment
7. Descriptive statistics
8. Logistic regression
9. Manuscript-style outputs
10. Hugging Face demo

## Repository Structure

```text
docs/       Project overview, analytic plan, data dictionary, mock IRB summary, and limitations
data/       Local raw and processed Synthea data folders excluded from version control
sql/        SQL scripts for cohort construction, outcome derivation, and validation
notebooks/  Notebook-based data profiling, analysis, modeling, and output generation
outputs/    Generated tables, figures, and QA artifacts
report/     Manuscript-style report materials and final written outputs
app/        Gradio app for presenting project context and selected outputs
scripts/    Command-line utilities for local data profiling and reproducible workflows
```

## Data Source

This project will use synthetic EHR data generated by Synthea. Synthea creates realistic but artificial patient records for testing, education, and demonstration.

This repository will not contain real patient data. It will also avoid committing large synthetic data files, local databases, or generated artifacts unless they are intentionally small and appropriate for portfolio review.

## Data Setup

This project uses Synthea synthetic CSV data. Raw CSV files should be placed locally in `data/raw/`.

Raw data is not committed to GitHub. Processed data, local databases, and generated profiling outputs are also excluded from version control unless a small artifact is intentionally added for portfolio review.

Before cohort construction, run one of the profiling workflows:

- `notebooks/01_synthea_data_profile.ipynb`
- `scripts/profile_synthea_data.py`

The profiling step checks which Synthea tables are available, reviews table shapes and columns, summarizes encounter class/type values, and assesses date fields and missingness before final cohort SQL is written.

The current profiling review is documented in `docs/06_synthea_profile_review.md`.

## Planned Outputs

- Cohort attrition table
- Missingness report
- Table 1 baseline characteristics
- Readmission summary table
- Outpatient follow-up timing summary
- ED revisit summary, if supported by encounter data
- Logistic regression results
- Cohort flow figure
- Odds ratio plot
- Brief results summary
- Hugging Face app

## Responsible Use

This project is educational and portfolio-focused. It uses synthetic data only and does not include real patient data. It is not intended for clinical decision-making, patient risk prediction, quality reporting, or operational deployment.

Analyses from this project should be interpreted as synthetic-data demonstrations of workflow design. The project does not make causal claims about outpatient follow-up, readmission, ED revisits, or any clinical outcome.
