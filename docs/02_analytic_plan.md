# Analytic Plan

## Study Objective

Evaluate demographic, clinical, and utilization factors associated with 30-day hospital readmission using synthetic EHR data.

## Research Question

Among adult patients with qualifying inpatient encounters, what factors are associated with 30-day hospital readmission?

## Study Design

Retrospective cohort study using synthetic EHR-style data.

## Data Source

This project will use Synthea synthetic EHR data. Synthea generates realistic but artificial patient records for education, testing, and demonstration. These data are synthetic and are not real patient records.

## Study Population

Adult patients with at least one qualifying inpatient encounter.

## Inclusion Criteria

- Age 18 or older at index encounter
- At least one inpatient encounter
- Valid encounter start and stop dates
- Valid patient identifier

## Exclusion Criteria

- Patients under age 18
- Encounters with missing or invalid start/end dates
- Encounters where discharge occurs before admission
- Duplicate or unresolved patient identifiers
- Patients without enough follow-up data to evaluate readmission, if applicable

## Index Encounter Definition

The index encounter is defined as the first qualifying inpatient encounter for each patient.

## Outcome Definition

Thirty-day readmission is defined as any subsequent inpatient encounter occurring within 30 days after discharge from the index encounter.

## Candidate Covariates

- Age
- Sex
- Race
- Ethnicity
- Length of stay
- Prior encounters
- Prior emergency visits if available
- Diabetes flag
- Hypertension flag
- Chronic kidney disease flag
- COPD flag
- Number of chronic conditions
- Discharge disposition if available

## Data Validation Plan

Planned data validation checks include:

- One index encounter per patient
- No negative length of stay
- Age 18+ only
- No missing primary outcome
- Duplicate patient IDs
- Missingness by variable
- Outcome distribution
- Cohort attrition counts

## Statistical Analysis Plan

The analysis will begin with descriptive statistics for the final analytic cohort. A Table 1 will compare patients with and without 30-day readmission.

Categorical variables will be compared using chi-square tests where appropriate. Continuous variables will be compared using t-tests or nonparametric alternatives where appropriate, depending on distributional assumptions and sample size.

Logistic regression will be used to estimate adjusted associations between candidate covariates and 30-day readmission. Model outputs will include odds ratios, 95% confidence intervals, and p-values.

## Planned Outputs

- Final analytic dataset
- Cohort attrition table
- Missingness report
- Table 1
- Readmission summary
- Logistic regression results table
- Cohort flow figure
- Odds ratio plot

## Limitations

This project uses synthetic data and is not supported by real-world clinical validation. Coding logic may simplify the complexity of real EHR workflows, including encounter classification, diagnosis grouping, discharge disposition, and follow-up observation windows.

Findings from this project will be educational and portfolio-focused. They should not be interpreted as clinical evidence or used for clinical decision-making.
