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

The study population will include adult patients with at least one qualifying inpatient encounter. The analytic dataset will be constructed at the patient-index encounter level, with one index encounter per patient.

## Inpatient Encounter Definition

Inpatient encounters will be identified using the Synthea `encounters` table and encounter classification fields when available, such as `encounter_class = 'inpatient'`. If the exact field names differ in the generated export, the SQL logic will be adapted to the available Synthea encounter type fields and documented in the SQL scripts.

Observation-only encounters and ED-only visits will not be counted as inpatient encounters for the primary readmission outcome. They may be summarized separately as utilization covariates if the encounter classification fields support that distinction.

## Inclusion Criteria

- Age 18 or older at index encounter
- At least one qualifying inpatient encounter
- Valid encounter start and stop dates
- Valid patient identifier

## Exclusion Criteria

- Patients under age 18
- Encounters with missing or invalid start/end dates
- Encounters where discharge occurs before admission
- Duplicate or unresolved patient identifiers
- Patients without enough follow-up data to evaluate readmission, if applicable

## Index Encounter Definition

The index encounter is defined as the first qualifying inpatient encounter for each patient. The first qualifying inpatient encounter will be used to reduce within-patient correlation and simplify interpretation of readmission outcomes in the initial project version.

## Outcome Definition

Thirty-day readmission is defined as any subsequent qualifying inpatient encounter occurring within 30 days after discharge from the index encounter.

The readmission window begins after the index encounter stop date. The primary outcome will be coded as `readmitted_30d = 1` when a subsequent inpatient encounter starts within 30 days after index discharge and `readmitted_30d = 0` otherwise, assuming sufficient follow-up data are available.

## Readmission Edge-Case Logic

- Same-day encounters after discharge may be reviewed separately as possible transfers or continuation-of-care events rather than automatically counted as readmissions.
- Observation-only encounters will not be counted as inpatient readmissions in the primary outcome.
- ED-only revisits may be summarized as utilization covariates but will not be counted as inpatient readmissions.
- Patients with death dates before completion of the 30-day follow-up window will be flagged for review and may be excluded from the primary outcome or included in a sensitivity analysis, depending on available fields.
- Patients discharged near the end of available observation data may be excluded or flagged if a complete 30-day follow-up window cannot be observed.

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

## Comorbidity Logic

Comorbidity flags will initially be derived from condition records occurring before or during the index encounter. The project will use simplified condition grouping logic appropriate for synthetic EHR data. Exact diagnosis grouping logic will be documented in SQL scripts and the data dictionary.

The initial comorbidity feature set will focus on diabetes, hypertension, chronic kidney disease, COPD, and a count of selected chronic conditions. Additional condition groupings may be added only if they improve interpretability and can be derived reproducibly from the available Synthea fields.

## Missingness Handling

Missingness will be assessed by variable after cohort construction and before modeling. Variables with minimal missingness may use complete-case analysis. Variables with substantial missingness will be assessed for exclusion, imputation feasibility, or reporting as a limitation depending on analytic importance.

The primary outcome, index encounter dates, patient identifier, and age eligibility fields are expected to be required for inclusion in the final analytic dataset. Records missing these core fields will be reviewed through validation checks before analysis.

## Data Validation Plan

Validation checks are intended to identify common retrospective EHR data issues including duplicated encounters, invalid temporal sequencing, impossible length-of-stay calculations, inconsistent patient identifiers, incomplete follow-up, and outcome derivation errors.

Planned validation checks include:

- One index encounter per patient
- No negative length of stay
- Age 18+ only
- No missing primary outcome
- Duplicate patient IDs
- Missingness by variable
- Outcome distribution
- Cohort attrition counts
- Encounter start and stop date ordering
- Thirty-day readmission window logic
- Follow-up completeness near the end of the available data

## Statistical Analysis Plan

The analysis will begin with descriptive statistics for the final analytic cohort. A Table 1 will compare patients with and without 30-day readmission.

Categorical variables will be compared using chi-square tests where appropriate. Continuous variables will be compared using t-tests or nonparametric alternatives where appropriate, depending on distributional assumptions and sample size.

Logistic regression was selected as the primary modeling approach because the outcome is binary and the model provides interpretable adjusted associations suitable for healthcare research reporting. Model outputs will include odds ratios, 95% confidence intervals, and p-values.

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

This project uses synthetic data and is not supported by real-world clinical validation. Coding logic may simplify the complexity of real EHR workflows, including encounter classification, diagnosis grouping, discharge disposition, transfers, observation stays, and follow-up observation windows.

Findings from this project will be educational and portfolio-focused. They should not be interpreted as clinical evidence or used for clinical decision-making.
