# Analytic Plan

## Study Objective

This project will develop and demonstrate a reproducible retrospective EHR analytics workflow for evaluating post-discharge utilization and 30-day inpatient readmission using Synthea synthetic data. The objective is to define an eligible adult inpatient cohort, derive outpatient follow-up and readmission timing measures, validate encounter-based outcome logic, and estimate associations between patient characteristics, utilization patterns, and 30-day readmission.

## Research Question

Among adult patients with a first eligible acute inpatient hospitalization in Synthea synthetic EHR data, what demographic, clinical, prior utilization, and discharge-related factors are associated with all-cause inpatient readmission within 30 days of discharge?

## Study Design

This project is structured as a retrospective cohort analysis using synthetic EHR-style encounter data. Adult patients with a first eligible inpatient encounter will be followed from the index discharge date through a 30-day post-discharge observation window. The analysis will derive readmission, outpatient follow-up, ED revisit, and post-discharge utilization measures from longitudinal encounter records. The design is intended to simulate a health system analytics request rather than produce clinically generalizable findings.

## Data Source

This project will use Synthea synthetic EHR data. Synthea generates realistic but artificial patient records for education, testing, and demonstration. These data are synthetic and are not real patient records.

## Literature-Informed Design Considerations

The analytic design is informed by published readmission studies and CMS readmission reporting examples. These sources reinforce several operational choices for this portfolio project:

- Use a clear index encounter and a 30-day post-discharge follow-up window.
- Distinguish inpatient readmissions from ED-only revisits and observation-only encounters.
- Evaluate prior utilization, including prior encounters and prior emergency visits.
- Consider comorbidity burden and selected chronic condition flags.
- Include discharge-related variables, such as discharge disposition or post-acute setting, when available.
- Assess equity-relevant patient characteristics, including race, ethnicity, sex, and payer, while avoiding clinical claims from synthetic data.

## Study Population

The study population will include adult patients with at least one eligible acute inpatient hospitalization. The analytic dataset will be constructed at the patient-index encounter level, with one index encounter per patient.

## Inpatient Encounter Definition

Inpatient encounters will be identified using the Synthea `encounters` table and encounter classification fields when available, such as `encounter_class = 'inpatient'`. If the exact field names differ in the generated export, the SQL logic will be adapted to the available Synthea encounter type fields and documented in the SQL scripts.

Observation-only encounters and ED-only visits will not be counted as inpatient encounters for the primary readmission outcome. They may be summarized separately as utilization covariates if the encounter classification fields support that distinction.

## Inclusion Criteria

- Age 18 or older at index encounter
- At least one eligible acute inpatient hospitalization
- Valid encounter start and stop dates
- Valid patient identifier

## Exclusion Criteria

- Patients under age 18
- Encounters with missing or invalid start/end dates
- Encounters where discharge occurs before admission
- Duplicate or unresolved patient identifiers
- Patients without enough follow-up data to evaluate readmission, if applicable

## Index Encounter Definition

The index encounter is defined as the first eligible acute inpatient hospitalization for each patient. The first eligible hospitalization will be used to reduce within-patient correlation and simplify interpretation of readmission outcomes in the initial project version.

## Outcome Definition

Thirty-day readmission is defined as any subsequent eligible inpatient encounter occurring within 30 days after discharge from the index encounter.

The readmission window begins after the index encounter stop date. The primary outcome will be coded as `readmitted_30d = 1` when a subsequent inpatient encounter starts within 30 days after index discharge and `readmitted_30d = 0` otherwise, assuming sufficient follow-up data are available.

The primary outcome will be all-cause inpatient readmission. If Synthea fields do not support a reliable planned versus unplanned readmission distinction, planned readmissions will not be separately excluded in the initial project version. This limitation will be documented in the report.

## Readmission Edge-Case Logic

- Same-day encounters after discharge may be reviewed separately as possible transfers or continuation-of-care events rather than automatically counted as readmissions.
- Observation-only encounters will not be counted as inpatient readmissions in the primary outcome.
- ED-only revisits may be summarized as utilization covariates but will not be counted as inpatient readmissions.
- Patients with death dates before completion of the 30-day follow-up window will be flagged for review and may be excluded from the primary outcome or included in a sensitivity analysis, depending on available fields.
- Patients discharged near the end of available observation data may be excluded or flagged if a complete 30-day follow-up window cannot be observed.
- If an ED encounter directly precedes an inpatient admission and appears to be part of the same acute episode, it may be linked to the inpatient encounter rather than treated as a separate readmission event.

## Candidate Covariates

- Age
- Sex
- Race
- Ethnicity
- Length of stay
- Prior encounters
- Prior inpatient encounters
- Prior emergency visits if available
- Prior institutional or post-acute exposure if available
- Primary diagnosis category if available
- Diabetes flag
- Hypertension flag
- Chronic kidney disease flag
- COPD flag
- Substance use flag if available
- Number of chronic conditions
- Payer if available
- Discharge disposition if available
- Post-acute discharge setting if available
- Discharge medication count and selected discharge-adjacent lab values if available

## Comorbidity Logic

Comorbidity flags will initially be derived from condition records occurring before or during the index encounter. The project will use simplified condition grouping logic appropriate for synthetic EHR data. Exact diagnosis grouping logic will be documented in SQL scripts and the data dictionary.

The initial comorbidity feature set will focus on diabetes, hypertension, chronic kidney disease, COPD, substance use if available, and a count of selected chronic conditions. Additional condition groupings may be added only if they improve interpretability and can be derived reproducibly from the available Synthea fields.

If available in the Synthea export, medication count near discharge and selected discharge-adjacent observations such as hemoglobin may be profiled as exploratory covariates. These variables will be treated as optional because availability and realism may vary across synthetic exports.

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
- Separation of inpatient readmissions from ED-only and observation-only revisits
- Frequency checks for discharge disposition, payer, and optional post-acute setting variables

## Statistical Analysis Plan

The analysis will begin with descriptive statistics for the final analytic cohort. A Table 1 will compare patients with and without 30-day readmission.

Categorical variables will be compared using chi-square tests where appropriate. Continuous variables will be compared using t-tests or nonparametric alternatives where appropriate, depending on distributional assumptions and sample size.

Logistic regression was selected as the primary modeling approach because the outcome is binary and the model provides interpretable adjusted associations suitable for healthcare research reporting. Model outputs will include odds ratios, 95% confidence intervals, and p-values.

Model covariates will be chosen based on clinical interpretability, literature-informed readmission domains, missingness, and availability in the synthetic export. The model will not be presented as a validated clinical risk prediction tool.

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
