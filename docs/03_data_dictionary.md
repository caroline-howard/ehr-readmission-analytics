# Data Dictionary

This draft data dictionary describes planned analytic variables for the Synthea EHR 30-day readmission workflow. Variable availability and exact source columns may change after the Synthea export is generated and profiled.

| Variable | Definition | Source | Type | Planned Derivation | Notes |
| --- | --- | --- | --- | --- | --- |
| patient_id | Unique synthetic patient identifier. | patients, encounters | String | Use the patient identifier linking patient-level records to encounters and clinical tables. | Required for cohort construction and table joins. |
| index_encounter_id | Unique identifier for the first qualifying inpatient encounter. | encounters | String | Select the first qualifying inpatient encounter for each eligible adult patient. | Used as the anchor encounter for outcome and covariate derivation. |
| birth_date | Patient date of birth. | patients | Date | Use the patient birth date field from the patients table. | Needed to calculate age at index encounter. |
| age_at_index | Patient age in years at the index encounter. | patients, encounters | Numeric | Calculate from birth date and index encounter start date. | Patients under age 18 will be excluded. |
| sex | Patient sex as represented in the synthetic source data. | patients | Categorical | Use the sex or gender field from the patients table, depending on export format. | Categories depend on Synthea output fields. |
| race | Patient race as represented in the synthetic source data. | patients | Categorical | Use the race field from the patients table. | Used for descriptive analysis and potential model adjustment. |
| ethnicity | Patient ethnicity as represented in the synthetic source data. | patients | Categorical | Use the ethnicity field from the patients table. | Used for descriptive analysis and potential model adjustment. |
| encounter_start | Start date and time of the index encounter. | encounters | Datetime | Use the start timestamp for the selected index encounter. | Must be valid and occur before encounter stop. |
| encounter_stop | End date and time of the index encounter. | encounters | Datetime | Use the stop timestamp for the selected index encounter. | Interpreted as discharge date/time for readmission logic. |
| length_of_stay_days | Duration of the index encounter in days. | encounters | Numeric | Calculate encounter stop minus encounter start. | Negative or invalid values should be excluded or resolved. |
| prior_encounters_12mo | Number of patient encounters in the 12 months before index admission. | encounters | Numeric | Count encounters for the same patient before index encounter start within a 12-month lookback window. | Encounter types included will be documented during implementation. |
| prior_ed_visits_12mo | Number of emergency department visits in the 12 months before index admission. | encounters | Numeric | Count prior encounters classified as emergency visits within a 12-month lookback window. | Availability depends on encounter class or type fields. |
| readmitted_30d | Indicator for any qualifying inpatient readmission within 30 days after index discharge. | encounters | Binary | Identify the next inpatient encounter after index encounter stop and flag if it occurs within 30 days. | Primary outcome variable. |
| days_to_readmission | Number of days from index discharge to readmission. | encounters | Numeric | Calculate days between index encounter stop and the start of the qualifying readmission encounter. | Missing or null if no qualifying readmission occurs. |
| diabetes_flag | Indicator for history of diabetes before or during the index encounter. | conditions | Binary | Flag patients with condition records consistent with diabetes before index discharge. | Coding logic will be documented after inspecting Synthea condition codes. |
| hypertension_flag | Indicator for history of hypertension before or during the index encounter. | conditions | Binary | Flag patients with condition records consistent with hypertension before index discharge. | Coding logic will be documented after inspecting Synthea condition codes. |
| ckd_flag | Indicator for history of chronic kidney disease before or during the index encounter. | conditions | Binary | Flag patients with condition records consistent with chronic kidney disease before index discharge. | Coding logic will be documented after inspecting Synthea condition codes. |
| copd_flag | Indicator for history of chronic obstructive pulmonary disease before or during the index encounter. | conditions | Binary | Flag patients with condition records consistent with COPD before index discharge. | Coding logic will be documented after inspecting Synthea condition codes. |
| chronic_condition_count | Count of selected chronic condition indicators for the patient. | conditions | Numeric | Sum selected condition flags or count distinct qualifying chronic condition categories before index discharge. | Exact condition set will be finalized during feature engineering. |
| death_date | Patient date of death, if present. | patients | Date | Use the death date field from the patients table when available. | May be missing for living patients or unavailable in some exports. |
| deceased_during_index | Indicator that the patient died during the index encounter. | patients, encounters | Binary | Compare death date with index encounter start and stop dates. | May be used for exclusion or sensitivity analysis. |
| payer | Patient payer or insurance category, if available. | payers, payer_transitions, encounters | Categorical | Use payer fields or join payer transition records to the index encounter period. | Availability depends on Synthea export settings and table structure. |
| discharge_disposition | Discharge status or disposition for the index encounter, if available. | encounters, observations | Categorical | Use encounter-level discharge disposition if present, or derive from related fields if supported. | Not guaranteed to be available in all Synthea exports. |

## Derived Variable Notes

- `age_at_index` is calculated from birth date and encounter start.
- `length_of_stay_days` is calculated from encounter stop minus encounter start.
- `readmitted_30d` is derived from the next inpatient encounter after discharge.
- Comorbidity flags are derived from condition records.
- Final variable availability may depend on the Synthea export format.
