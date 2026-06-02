# Cohort Attrition Report

## Purpose

This report audits why the final analytic cohort contains 255 patients even though the source Synthea dataset contains 1,163 synthetic patients. The objective is transparency, not changing the cohort logic.

The current analytic workflow is intentionally focused on adult patients with a valid inpatient index hospitalization so that 30-day post-discharge utilization and readmission measures can be derived consistently.

## Starting and Final Population

| Measure | Count |
| --- | ---: |
| Starting synthetic patients | 1,163 |
| Final analytic cohort | 255 |
| Patients excluded before final cohort | 908 |
| Percent of source patients retained | 21.9% |

## Why Did 1,163 Synthetic Patients Become 255 Analytic Patients?

The cohort was reduced primarily because most source patients did not have an inpatient encounter. This project is designed around 30-day readmission after discharge from an index inpatient hospitalization, so patients without an inpatient encounter cannot enter the analytic cohort.

The exact reconciliation is:

```text
1,163 starting synthetic patients
-   0 patients without any encounter
- 878 patients without any inpatient encounter
-   0 patients excluded for invalid patient linkage, missing birth date, invalid inpatient dates, or discharge before admission
-  30 patients under age 18 across valid inpatient encounters
-   0 patients excluded during index admission selection
-   0 patients excluded during 30-day utilization/readmission outcome derivation
= 255 final analytic patients
```

## Cohort Attrition Table

| Step | Cohort Step | Patients Remaining | Excluded at Step | Percent Remaining | Exclusion Reason |
| ---: | --- | ---: | ---: | ---: | --- |
| 0 | All Synthea Patients | 1,163 | 0 | 100.0% | Starting population from `patients.csv`. |
| 1 | Patients With Any Encounter | 1,163 | 0 | 100.0% | No patients excluded; every source patient had at least one encounter record. |
| 2 | Patients With Any Inpatient Encounter | 285 | 878 | 24.5% | Excluded patients without an inpatient encounter because the readmission workflow requires an index hospitalization. |
| 3 | Valid Patient Linkage, Birth Date, and Inpatient Dates | 285 | 0 | 24.5% | No additional patients excluded; inpatient encounters linked to patients, had birth dates, valid admission dates, valid discharge dates, and discharge was not before admission. |
| 4 | Adult Patients With Eligible Inpatient Encounter | 255 | 30 | 21.9% | Excluded patients who were under age 18 across valid inpatient encounters. |
| 5 | First Eligible Inpatient Encounter Selected as Index Admission | 255 | 0 | 21.9% | No patients excluded; the first eligible inpatient encounter was selected to create one index admission per patient. |
| 6 | 30-Day Follow-Up and Readmission Outcome Derived | 255 | 0 | 21.9% | No patients excluded; 30-day post-discharge utilization and readmission fields were derived for every index patient. |
| 7 | Final Analytic Cohort | 255 | 0 | 21.9% | Final analysis dataset rows match the dashboard KPI cohort count. |

## Cohort Rules Audited

The audit traced the current cohort construction workflow across:

- `sql/01_profile_source_tables.sql`
- `sql/02_define_eligible_inpatient_encounters.sql`
- `sql/03_define_index_encounter.sql`
- `sql/04_define_postdischarge_utilization.sql`
- `sql/05_define_30_day_readmission.sql`
- `sql/06_create_final_analysis_dataset.sql`
- `outputs/validation/cohort_attrition_counts.csv`
- `outputs/bi/cohort_summary_table.csv`
- `notebooks/04_cohort_attrition_analysis.ipynb`

Intermediate SQL views reviewed:

- `eligible_inpatient_encounters`
- `index_encounter`
- `postdischarge_utilization`
- `readmission_outcomes`
- `final_analysis_dataset`

Downstream notebook review:

- `notebooks/02_descriptive_analysis.ipynb` loads `final_analysis_dataset` and generates aggregate descriptive outputs. It does not further reduce the final analytic cohort.
- `notebooks/03_logistic_regression.ipynb` uses the final analysis dataset for exploratory modeling. Modeling-specific complete-case handling is separate from the cohort definition and does not explain the 255-patient analytic cohort.

The main cohort rules are:

- Start with all patients in the Synthea `patients.csv` file.
- Confirm whether each patient has encounter records.
- Restrict to patients with at least one inpatient encounter.
- Require inpatient encounters to link to a valid patient identifier.
- Require valid birth date, admission date, discharge date, and discharge not before admission.
- Restrict to adult patients age 18 or older at a valid inpatient encounter.
- Select the first eligible inpatient encounter as the index admission.
- Derive 30-day post-discharge utilization and readmission outcomes for every index patient.
- Create one final analytic row per index patient.

## Validation Checks

| Validation Check | Result |
| --- | --- |
| Every exclusion is accounted for | Pass |
| Starting patients minus documented exclusions equals final cohort | 1,163 - 908 = 255 |
| Final cohort count matches dashboard KPI count | Pass: 255 final rows and 255 dashboard cohort patients |
| Duplicate patient index rows | 0 |
| Missing patient IDs in final dataset | 0 |
| Missing index encounter IDs in final dataset | 0 |
| Under-18 index rows in final dataset | 0 |
| Negative length-of-stay rows in final dataset | 0 |
| Discharge-before-admission rows in final dataset | 0 |
| Missing 30-day readmission outcome rows | 0 |

## Top Drivers of Cohort Reduction

| Rank | Driver | Patients Excluded | Impact |
| ---: | --- | ---: | --- |
| 1 | No inpatient encounter | 878 | Largest reduction. These patients cannot contribute to a readmission-after-discharge cohort because they do not have an eligible inpatient hospitalization. |
| 2 | Under age 18 at valid inpatient encounter | 30 | Adult-only study population rule. |
| 3 | No encounter records | 0 | All source patients had at least one encounter. |
| 4 | Invalid patient linkage, missing birth date, invalid inpatient dates, or discharge before admission | 0 | No patient-level exclusions from these rules in the current Synthea export. |
| 5 | Index admission selection | 0 | Selecting the first eligible inpatient encounter reduces encounter rows but not patient count. |
| 6 | 30-day utilization/readmission derivation | 0 | Outcomes were populated for all final index patients. |

## Interpretation

The final cohort of 255 patients is not a data loss problem. It is the result of applying a clinically coherent analytic definition: adult patients with a valid inpatient hospitalization that can serve as an index admission for post-discharge utilization and 30-day readmission analysis.

The largest reduction is expected for this type of retrospective readmission workflow because many synthetic patients have outpatient, ambulatory, wellness, urgent care, or emergency encounters but never have an inpatient hospitalization.

These findings are based on synthetic Synthea EHR data and should be interpreted as portfolio workflow documentation, not as clinical evidence or a statement about real-world hospitalization rates.

## Related Outputs

- Cohort attrition table: `outputs/cohort_attrition.csv`
- Cohort flow dataset: `outputs/cohort_flow_summary.csv`
- Cohort flow figure: `outputs/figures/cohort_attrition_audit.png`
- Reproducible notebook: `notebooks/04_cohort_attrition_analysis.ipynb`
