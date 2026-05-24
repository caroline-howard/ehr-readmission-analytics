# Analytic Plan

## Study Objective

Evaluate post-discharge utilization patterns and factors associated with all-cause 30-day inpatient readmission after a first eligible acute inpatient hospitalization using synthetic EHR data.

## Research Question

Among adult patients with a first eligible acute inpatient hospitalization in Synthea synthetic EHR data, how are outpatient follow-up timing, demographic characteristics, clinical conditions, prior utilization, and discharge-related factors associated with all-cause inpatient readmission within 30 days of discharge?

## Study Design

Retrospective cohort study using synthetic EHR-style data.

## Data Source

This project will use Synthea synthetic EHR data. Synthea generates realistic but artificial patient records for education, testing, and demonstration. These data are synthetic and are not real patient records.

## Literature-Informed Design Considerations

The analytic design is informed by outpatient follow-up and readmission literature, including Balasubramanian et al. (2025), as well as published readmission studies and CMS readmission reporting examples. These sources reinforce several operational choices for this portfolio project:

- Use a clear index encounter and a 30-day post-discharge follow-up window.
- Derive outpatient follow-up timing across 7-day, 14-day, and 30-day windows.
- Distinguish inpatient readmissions from ED-only revisits and observation-only encounters.
- Treat readmission, ED revisit, outpatient follow-up, and mortality as related but distinct post-discharge measures.
- Evaluate prior utilization, including prior encounters and prior emergency visits.
- Consider comorbidity burden and selected chronic condition flags.
- Explore age, disease group, and baseline risk strata when supported by the synthetic data.
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

## Primary Outcome

Thirty-day readmission is defined as any subsequent eligible inpatient encounter occurring within 30 days after discharge from the index encounter.

The readmission window begins after the index encounter stop date. The primary outcome will be coded as `readmitted_30d = 1` when a subsequent inpatient encounter starts within 30 days after index discharge and `readmitted_30d = 0` otherwise, assuming sufficient follow-up data are available.

The primary outcome will be all-cause inpatient readmission. If Synthea fields do not support a reliable planned versus unplanned readmission distinction, planned readmissions will not be separately excluded in the initial project version. This limitation will be documented in the report.

## Variable Scope

To keep the first project version feasible, variables will be separated into a core MVP set and optional exploratory variables.

Core MVP variables are required for the initial cohort build, validation workflow, descriptive analysis, and primary model:

- Patient identifier
- Index encounter identifier
- Age at index
- Sex
- Race
- Ethnicity
- Index encounter start and stop dates
- Length of stay
- Prior encounters in the 12 months before index admission
- Prior ED visits in the 12 months before index admission, if ED encounter class is identifiable
- Outpatient follow-up within 7, 14, and 30 days
- Days to first outpatient follow-up
- ED revisit within 30 days, if ED encounter class is identifiable
- Thirty-day inpatient readmission outcome
- Days to readmission
- Core comorbidity flags: diabetes, hypertension, chronic kidney disease, and COPD
- Chronic condition count

Optional exploratory variables may be profiled or added only if the Synthea export supports defensible derivation:

- Payer
- Discharge disposition
- Post-acute discharge setting
- Disease or condition subgroup
- AMI-like cardiovascular condition grouping
- Substance use flag
- Death during index admission
- Death within 30 days after discharge
- Medication count at discharge
- Discharge-adjacent lab values
- Functional status proxies
- Prior institutional exposure

## Secondary Post-Discharge Utilization Measures

Core secondary measures will describe utilization after discharge from the index inpatient encounter:

- `outpatient_followup_7d`
- `outpatient_followup_14d`
- `outpatient_followup_30d`
- `ed_revisit_30d`, if encounter data support ED classification
- `days_to_first_outpatient_followup`
- `days_to_first_postdischarge_encounter`
- `total_postdischarge_encounters_30d`

Optional secondary measures may include:

- Death within the 30-day post-discharge window, if death data are available

These measures are intended to describe post-discharge utilization patterns and support exploratory modeling. They will not be interpreted as causal effects.

## Outpatient Follow-Up Definition

Outpatient follow-up is defined as an outpatient or ambulatory encounter occurring after discharge from the index inpatient encounter and within the specified follow-up window.

ED-only encounters will not count as outpatient follow-up. Observation encounters, inpatient encounters, and same-episode transfer-like encounters will not count as outpatient follow-up. If Synthea encounter class fields differ from expected values, the SQL implementation will map the available encounter types to the closest defensible categories and document the decision.

## Timing Windows

Outpatient follow-up will be evaluated in three post-discharge windows:

- 0-7 days after discharge
- 0-14 days after discharge
- 0-30 days after discharge

The same 30-day post-discharge window will be used for the primary readmission outcome and ED revisit measure.

## Temporal Sequencing and Bias-Aware Logic

Patients readmitted before an outpatient follow-up occurs create time-dependent interpretation problems because they may not have had an opportunity to complete follow-up. This project will derive timing variables and flag cases where the readmission occurs before outpatient follow-up.

Outpatient visits after a readmission will not be treated as preventing that readmission. The initial portfolio version will report associations only and will avoid causal language about outpatient follow-up reducing readmission.

## Readmission Edge-Case Logic

- Same-day encounters after discharge may be reviewed separately as possible transfers or continuation-of-care events rather than automatically counted as readmissions.
- Observation-only encounters will not be counted as inpatient readmissions in the primary outcome.
- ED-only revisits may be summarized as utilization covariates but will not be counted as inpatient readmissions.
- Outpatient visits after a readmission will not be counted as follow-up exposure before that readmission.
- Deaths during the index admission will be excluded from the primary cohort if death data are available.
- Deaths after discharge but before 30 days will be flagged if death data are available.
- Patients with death dates before completion of the 30-day follow-up window will be flagged for review and may be excluded from the primary outcome or included in a sensitivity analysis, depending on available fields.
- Patients discharged near the end of available observation data may be excluded or flagged if a complete 30-day follow-up window cannot be observed.
- If an ED encounter directly precedes an inpatient admission and appears to be part of the same acute episode, it may be linked to the inpatient encounter rather than treated as a separate readmission event.

## Age and Risk Stratification

Planned descriptive stratification will include:

- Age group, such as under 65 versus 65 and older
- Chronic condition count
- Prior utilization burden
- Length of stay category

These strata are intended to describe whether follow-up patterns and readmission rates differ across patient risk profiles. They will not establish clinical effectiveness.

## Disease and Condition Grouping

If feasible with Synthea data, the project may document simplified disease groupings for common readmission-relevant conditions, such as heart failure, COPD, diabetes, hypertension, chronic kidney disease, and AMI-like cardiovascular conditions. These groupings are optional exploratory variables, not required for the MVP workflow.

If the generated Synthea export does not support reliable disease grouping, the project will use available condition records and simplified groupings suitable for synthetic EHR data. Exact grouping logic will be documented in SQL scripts and the data dictionary.

## Core Candidate Covariates

- Age
- Sex
- Race
- Ethnicity
- Length of stay
- Prior encounters
- Prior emergency visits if available
- Outpatient follow-up within 7, 14, and 30 days
- ED revisit within 30 days if available
- Days to first post-discharge encounter
- Diabetes flag
- Hypertension flag
- Chronic kidney disease flag
- COPD flag
- Number of chronic conditions

## Optional Exploratory Covariates

- Prior inpatient encounters
- Prior institutional or post-acute exposure if available
- Primary diagnosis category if available
- Disease or condition subgroup if reproducible from condition records
- Substance use flag if available
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
- Outpatient follow-up timing window logic
- Cases where readmission occurs before outpatient follow-up
- Follow-up completeness near the end of the available data
- Separation of inpatient readmissions from ED-only and observation-only revisits
- Frequency checks for discharge disposition, payer, and optional post-acute setting variables

## Statistical Analysis Plan

The analysis will begin with descriptive statistics for the final analytic cohort. A Table 1 will compare patients with and without 30-day readmission.

Categorical variables will be compared using chi-square tests where appropriate. Continuous variables will be compared using t-tests or nonparametric alternatives where appropriate, depending on distributional assumptions and sample size.

Logistic regression was selected as the primary modeling approach because the outcome is binary and the model provides interpretable adjusted associations suitable for healthcare research reporting. Model outputs will include odds ratios, 95% confidence intervals, and p-values.

Model covariates will be chosen based on clinical interpretability, literature-informed readmission domains, missingness, and availability in the synthetic export. The model will not be presented as a validated clinical risk prediction tool.

Outpatient follow-up variables may be included as exploratory covariates only, with careful interpretation due to temporal sequencing, confounding by illness severity, and differences in baseline readmission risk. The analysis will describe associations and will not claim that follow-up causes changes in readmission.

## Planned Outputs

- Final analytic dataset
- Cohort attrition table
- Missingness report
- Table 1
- Readmission summary
- Outpatient follow-up timing summary
- ED revisit summary, if supported by encounter data
- Logistic regression results table
- Cohort flow figure
- Odds ratio plot

## Limitations

This project uses synthetic data and is not supported by real-world clinical validation. Coding logic may simplify the complexity of real EHR workflows, including encounter classification, diagnosis grouping, discharge disposition, transfers, observation stays, and follow-up observation windows.

Findings from this project will be educational and portfolio-focused. They should not be interpreted as clinical evidence or used for clinical decision-making.
