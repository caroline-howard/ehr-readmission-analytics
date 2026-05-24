# Analytic Plan

## Research Question

Among patients with an eligible inpatient encounter in synthetic EHR data, what patient and encounter characteristics are associated with 30-day hospital readmission?

## Study Design

Retrospective cohort study using Synthea synthetic EHR data.

## Data Source

The planned source data are Synthea CSV exports representing synthetic patients, encounters, conditions, medications, procedures, observations, and related EHR tables. The exact tables used will be documented after data ingestion.

## Target Population

The planned cohort will include patients with at least one eligible inpatient encounter during the study period. Eligibility rules will be finalized after reviewing available Synthea encounter classes, dates, and table structure.

## Index Encounter

The index encounter will be an eligible inpatient hospitalization. If a patient has multiple eligible hospitalizations, the project will define whether to use the first eligible hospitalization, all eligible hospitalizations, or a sensitivity analysis approach.

## Primary Outcome

The primary outcome is all-cause hospital readmission within 30 days after discharge from the index encounter.

Planned outcome logic:

- Identify discharge date for the index encounter.
- Search for a subsequent inpatient encounter for the same patient.
- Classify readmission as present if the subsequent inpatient encounter begins within 30 days after discharge.
- Exclude same-day transfers or continuation encounters if the source data support that distinction.

## Candidate Covariates

Planned covariate domains include:

- Demographics: age, sex, race, ethnicity, and insurance or payer if available
- Encounter characteristics: length of stay, admission type, discharge disposition if available
- Clinical history: selected chronic conditions or diagnosis groupings
- Utilization history: prior encounters or prior inpatient use
- Medication or procedure indicators if supported by data quality

## Analysis Plan

The initial analysis will include:

- Cohort counts and inclusion/exclusion flow
- Descriptive statistics stratified by readmission status
- Missingness and data quality checks
- Bivariate comparisons where appropriate
- A parsimonious regression model or classification model if the data support it

Any model outputs will be interpreted as portfolio demonstrations using synthetic data, not as clinically generalizable findings.

## Validation Plan

Validation will focus on:

- Unique patient and encounter counts
- Encounter date ordering
- Length-of-stay plausibility
- Outcome date logic
- Duplicate rows and unexpected null values
- Reproducibility of cohort counts from raw tables to analytic dataset
