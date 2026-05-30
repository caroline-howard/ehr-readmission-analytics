# Synthea Profiling Review

This review summarizes the local Synthea CSV profiling results used to confirm whether the planned post-discharge utilization and 30-day readmission workflow is feasible before writing final cohort SQL.

The review is based on synthetic CSV files stored locally in `data/raw/`. Raw data files are intentionally excluded from version control. These findings are data profiling notes, not clinical results.

## Source Tables Reviewed

| Table | Rows | Columns | Review Purpose |
| --- | ---: | ---: | --- |
| patients | 1,163 | 25 | Patient identifiers, demographics, birth date, and death date availability |
| encounters | 61,459 | 15 | Encounter classes, start/stop dates, patient joins, and utilization timing |
| conditions | 38,094 | 6 | Condition history and candidate comorbidity flags |

## Encounter Classification Findings

The `encounters.csv` file includes an `encounterclass` field that supports the core utilization definitions.

| Encounter class | Count | Planned Use |
| --- | ---: | --- |
| wellness | 24,038 | Excluded from inpatient readmission; may be reviewed separately if needed |
| ambulatory | 20,124 | Candidate outpatient follow-up class |
| outpatient | 10,837 | Candidate outpatient follow-up class |
| urgentcare | 2,564 | Optional utilization category; not part of core MVP outcome |
| emergency | 2,168 | Candidate ED revisit class |
| inpatient | 1,728 | Candidate index hospitalization and readmission class |

## Encounter Type Assessment

Inpatient, outpatient or ambulatory, and emergency encounters are distinguishable in this Synthea export.

Planned operational mapping for the first cohort build:

- Index hospitalization and readmission: `encounterclass = 'inpatient'`
- Outpatient follow-up: `encounterclass in ('outpatient', 'ambulatory')`
- ED revisit: `encounterclass = 'emergency'`
- Urgent care: optional secondary utilization category, not part of the core MVP
- Wellness: exclude from primary post-discharge follow-up unless a later clinical review supports including specific wellness visits

No separate observation encounter class was identified in the profiled export. Observation-specific logic should remain optional unless a future Synthea export includes a defensible observation category.

## Encounter Date Completeness

Encounter start and stop dates are complete and parse cleanly.

| Check | Result |
| --- | ---: |
| Missing encounter start timestamps | 0 |
| Missing encounter stop timestamps | 0 |
| Unparseable encounter start timestamps | 0 |
| Unparseable encounter stop timestamps | 0 |
| Encounters where stop occurs before start | 0 |
| Encounters with identical start and stop timestamps | 0 |

The available date structure supports length-of-stay calculation, index discharge timing, outpatient follow-up windows, ED revisit timing, and 30-day readmission derivation.

## Patient Identifier Join Review

Patient identifiers join cleanly across the core patient, encounter, and condition tables.

| Check | Result |
| --- | ---: |
| Encounter patient IDs missing from patients table | 0 |
| Condition patient IDs missing from patients table | 0 |
| Patients without encounters | 0 |
| Patients without conditions | 16 |
| Condition encounter IDs missing from encounters table | 0 |
| Encounters without condition records | 34,555 |
| Duplicate patient IDs | 0 |
| Duplicate encounter IDs | 0 |

The 16 patients without condition records and the encounters without condition records are expected profiling findings rather than join failures. Cohort SQL should avoid assuming that every patient or encounter has an associated condition record.

## Comorbidity Flag Feasibility

Condition records support the planned core comorbidity flags, but grouping rules should be explicit in SQL and the data dictionary.

| Candidate flag | Matching condition rows | Patients with matching records | Profiling interpretation |
| --- | ---: | ---: | --- |
| Diabetes | 509 | 364 | Feasible, but `Prediabetes` appears frequently and should be excluded or handled separately from a diabetes flag |
| Hypertension | 292 | 292 | Feasible using the hypertension condition description/code |
| Chronic kidney disease | 62 | 31 | Feasible, but logic should distinguish CKD-stage records from diabetic renal disease if needed |
| COPD | 12 | 12 | Feasible, represented as chronic obstructive bronchitis in this export |

Example condition descriptions identified during profiling include:

- Diabetes
- Prediabetes
- Diabetic renal disease
- Hypertension
- Chronic kidney disease stage 1
- Chronic kidney disease stage 2
- Chronic obstructive bronchitis

## Recommended SQL Implementation Notes

- Use normalized lowercase column names in scripts to avoid case-sensitivity issues across Synthea exports.
- Define the first eligible index hospitalization using `encounterclass = 'inpatient'`.
- Use `outpatient` and `ambulatory` encounter classes for outpatient follow-up measures.
- Use `emergency` encounter class for ED revisit measures.
- Keep urgent care and wellness encounters separate from the core MVP definitions unless a later analytic decision explicitly includes them.
- Do not require a condition record for cohort inclusion unless the specific analysis requires a condition-based subgroup.
- Document diagnosis code and description groupings for diabetes, hypertension, CKD, and COPD before feature derivation.
- Treat prediabetes separately from diabetes unless the analytic plan intentionally broadens the definition.

## Readiness Assessment

The profiled Synthea export supports the next project step: writing cohort construction and validation SQL for an adult first eligible inpatient hospitalization cohort, followed by derivation of post-discharge outpatient follow-up, ED revisit, and 30-day inpatient readmission measures.

The next implementation milestone should focus on SQL cohort logic, with validation queries for encounter class mapping, date sequencing, one index encounter per patient, post-discharge timing windows, and comorbidity flag derivation.
