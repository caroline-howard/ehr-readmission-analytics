# Data Dictionary

This file will document raw source tables and derived analytic variables used in the project. It is intentionally preliminary until Synthea data are generated, loaded, and profiled.

## Planned Analytic Variables

| Variable | Planned Type | Description | Source or Derivation |
| --- | --- | --- | --- |
| patient_id | String | Unique synthetic patient identifier | Synthea patients table |
| index_encounter_id | String | Eligible inpatient encounter selected as the index encounter | Synthea encounters table |
| index_admit_date | Date/datetime | Start date of the index inpatient encounter | Encounters start date |
| index_discharge_date | Date/datetime | End date of the index inpatient encounter | Encounters stop date |
| length_of_stay_days | Numeric | Duration of index hospitalization in days | Discharge date minus admit date |
| readmitted_30d | Binary | Indicator for inpatient readmission within 30 days of discharge | Derived from subsequent encounters |
| readmission_encounter_id | String | Encounter identifier for the qualifying readmission, if present | Derived from encounters |
| readmission_days_after_discharge | Numeric | Days from index discharge to readmission start | Derived from encounter dates |
| age_at_index | Numeric | Patient age at index admission | Birth date and index admission date |
| sex | Categorical | Patient sex as represented in source data | Patients table |
| race | Categorical | Patient race as represented in source data | Patients table |
| ethnicity | Categorical | Patient ethnicity as represented in source data | Patients table |
| payer | Categorical | Insurance or payer category, if available | Payer fields or payer transition tables |
| chronic_condition_count | Numeric | Count of selected chronic conditions before index discharge | Derived from conditions |
| prior_inpatient_count | Numeric | Number of inpatient encounters before index admission | Derived from encounters |

## Data Dictionary Maintenance

As SQL scripts and notebooks are developed, each derived variable should include:

- Business definition
- Source table and column lineage
- Inclusion and exclusion rules
- Data type
- Allowed values or units
- Missingness handling
