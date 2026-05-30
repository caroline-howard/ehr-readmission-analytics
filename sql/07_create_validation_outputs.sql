-- Create aggregate QA validation outputs before descriptive statistics or modeling.
-- Requires sql/01 through sql/06 to be run first in the same DuckDB database.
-- Outputs are aggregate synthetic-data QA tables, not patient-level records.

CREATE OR REPLACE VIEW validation_cohort_attrition_counts AS
SELECT 'source_patients' AS step, COUNT(*) AS record_count FROM raw_patients
UNION ALL
SELECT 'source_encounters' AS step, COUNT(*) AS record_count FROM raw_encounters
UNION ALL
SELECT 'source_inpatient_encounters' AS step, COUNT(*) AS record_count
FROM raw_encounters
WHERE LOWER(encounterclass) = 'inpatient'
UNION ALL
SELECT 'eligible_adult_inpatient_encounters' AS step, COUNT(*) AS record_count
FROM eligible_inpatient_encounters
UNION ALL
SELECT 'patients_with_eligible_adult_inpatient_encounter' AS step, COUNT(DISTINCT patient_id) AS record_count
FROM eligible_inpatient_encounters
UNION ALL
SELECT 'index_encounters' AS step, COUNT(*) AS record_count
FROM index_encounter
UNION ALL
SELECT 'final_analysis_dataset_rows' AS step, COUNT(*) AS record_count
FROM final_analysis_dataset;

CREATE OR REPLACE VIEW validation_index_encounter_check AS
SELECT
    COUNT(*) AS index_rows,
    COUNT(DISTINCT patient_id) AS distinct_patients,
    COUNT(*) - COUNT(DISTINCT patient_id) AS duplicate_patient_index_rows,
    SUM(CASE WHEN patient_id IS NULL THEN 1 ELSE 0 END) AS missing_patient_id_rows,
    SUM(CASE WHEN index_encounter_id IS NULL THEN 1 ELSE 0 END) AS missing_index_encounter_id_rows,
    SUM(CASE WHEN age_at_index < 18 THEN 1 ELSE 0 END) AS under_18_index_rows,
    SUM(CASE WHEN length_of_stay_days < 0 THEN 1 ELSE 0 END) AS negative_length_of_stay_rows,
    SUM(CASE WHEN encounter_stop < encounter_start THEN 1 ELSE 0 END) AS discharge_before_admission_rows
FROM final_analysis_dataset;

CREATE OR REPLACE VIEW validation_date_validity_checks AS
SELECT
    'raw_encounters' AS dataset,
    COUNT(*) AS row_count,
    SUM(CASE WHEN start IS NULL THEN 1 ELSE 0 END) AS missing_start,
    SUM(CASE WHEN stop IS NULL THEN 1 ELSE 0 END) AS missing_stop,
    SUM(CASE WHEN TRY_CAST(start AS TIMESTAMP) IS NULL THEN 1 ELSE 0 END) AS invalid_start,
    SUM(CASE WHEN TRY_CAST(stop AS TIMESTAMP) IS NULL THEN 1 ELSE 0 END) AS invalid_stop,
    SUM(
        CASE
            WHEN TRY_CAST(stop AS TIMESTAMP) < TRY_CAST(start AS TIMESTAMP)
            THEN 1 ELSE 0
        END
    ) AS stop_before_start
FROM raw_encounters
UNION ALL
SELECT
    'final_analysis_dataset' AS dataset,
    COUNT(*) AS row_count,
    SUM(CASE WHEN encounter_start IS NULL THEN 1 ELSE 0 END) AS missing_start,
    SUM(CASE WHEN encounter_stop IS NULL THEN 1 ELSE 0 END) AS missing_stop,
    SUM(CASE WHEN TRY_CAST(encounter_start AS TIMESTAMP) IS NULL THEN 1 ELSE 0 END) AS invalid_start,
    SUM(CASE WHEN TRY_CAST(encounter_stop AS TIMESTAMP) IS NULL THEN 1 ELSE 0 END) AS invalid_stop,
    SUM(CASE WHEN encounter_stop < encounter_start THEN 1 ELSE 0 END) AS stop_before_start
FROM final_analysis_dataset;

CREATE OR REPLACE VIEW validation_encounter_class_distribution AS
SELECT
    LOWER(encounterclass) AS encounter_class,
    COUNT(*) AS encounter_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS encounter_percent
FROM raw_encounters
GROUP BY LOWER(encounterclass)
ORDER BY encounter_count DESC;

CREATE OR REPLACE VIEW validation_missingness_report AS
WITH base AS (
    SELECT * FROM final_analysis_dataset
),
missingness AS (
    SELECT 'patient_id' AS variable, COUNT(*) AS row_count, SUM(CASE WHEN patient_id IS NULL THEN 1 ELSE 0 END) AS missing_count FROM base
    UNION ALL SELECT 'index_encounter_id', COUNT(*), SUM(CASE WHEN index_encounter_id IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'birth_date', COUNT(*), SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'age_at_index', COUNT(*), SUM(CASE WHEN age_at_index IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'sex', COUNT(*), SUM(CASE WHEN sex IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'race', COUNT(*), SUM(CASE WHEN race IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'ethnicity', COUNT(*), SUM(CASE WHEN ethnicity IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'encounter_start', COUNT(*), SUM(CASE WHEN encounter_start IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'encounter_stop', COUNT(*), SUM(CASE WHEN encounter_stop IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'length_of_stay_days', COUNT(*), SUM(CASE WHEN length_of_stay_days IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'prior_encounters_12mo', COUNT(*), SUM(CASE WHEN prior_encounters_12mo IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'prior_ed_visits_12mo', COUNT(*), SUM(CASE WHEN prior_ed_visits_12mo IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'outpatient_followup_7d', COUNT(*), SUM(CASE WHEN outpatient_followup_7d IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'outpatient_followup_14d', COUNT(*), SUM(CASE WHEN outpatient_followup_14d IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'outpatient_followup_30d', COUNT(*), SUM(CASE WHEN outpatient_followup_30d IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'days_to_first_outpatient_followup', COUNT(*), SUM(CASE WHEN days_to_first_outpatient_followup IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'ed_revisit_30d', COUNT(*), SUM(CASE WHEN ed_revisit_30d IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'days_to_first_postdischarge_encounter', COUNT(*), SUM(CASE WHEN days_to_first_postdischarge_encounter IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'total_postdischarge_encounters_30d', COUNT(*), SUM(CASE WHEN total_postdischarge_encounters_30d IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'readmitted_30d', COUNT(*), SUM(CASE WHEN readmitted_30d IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'readmission_encounter_id', COUNT(*), SUM(CASE WHEN readmission_encounter_id IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'days_to_readmission', COUNT(*), SUM(CASE WHEN days_to_readmission IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'readmission_before_outpatient_followup_flag', COUNT(*), SUM(CASE WHEN readmission_before_outpatient_followup_flag IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'possible_same_day_transfer_flag', COUNT(*), SUM(CASE WHEN possible_same_day_transfer_flag IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'diabetes_flag', COUNT(*), SUM(CASE WHEN diabetes_flag IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'hypertension_flag', COUNT(*), SUM(CASE WHEN hypertension_flag IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'ckd_flag', COUNT(*), SUM(CASE WHEN ckd_flag IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'copd_flag', COUNT(*), SUM(CASE WHEN copd_flag IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'chronic_condition_count', COUNT(*), SUM(CASE WHEN chronic_condition_count IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'death_date', COUNT(*), SUM(CASE WHEN death_date IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'deceased_during_index', COUNT(*), SUM(CASE WHEN deceased_during_index IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'postdischarge_death_30d', COUNT(*), SUM(CASE WHEN postdischarge_death_30d IS NULL THEN 1 ELSE 0 END) FROM base
    UNION ALL SELECT 'payer', COUNT(*), SUM(CASE WHEN payer IS NULL THEN 1 ELSE 0 END) FROM base
)
SELECT
    variable,
    row_count,
    missing_count,
    ROUND(100.0 * missing_count / NULLIF(row_count, 0), 2) AS missing_percent
FROM missingness
ORDER BY missing_percent DESC, variable;

CREATE OR REPLACE VIEW validation_readmission_timing AS
SELECT
    COUNT(*) AS final_rows,
    SUM(readmitted_30d) AS readmitted_30d_count,
    SUM(CASE WHEN readmitted_30d IS NULL THEN 1 ELSE 0 END) AS missing_readmission_outcome_rows,
    SUM(CASE WHEN readmitted_30d = 1 AND days_to_readmission IS NULL THEN 1 ELSE 0 END)
        AS readmitted_missing_days_to_readmission_rows,
    SUM(CASE WHEN days_to_readmission < 0 THEN 1 ELSE 0 END) AS negative_days_to_readmission_rows,
    SUM(CASE WHEN days_to_readmission > 30 THEN 1 ELSE 0 END) AS over_30_day_readmission_rows,
    SUM(possible_same_day_transfer_flag) AS possible_same_day_transfer_count,
    SUM(readmission_before_outpatient_followup_flag) AS readmission_before_outpatient_followup_count,
    MIN(days_to_readmission) AS min_days_to_readmission,
    MAX(days_to_readmission) AS max_days_to_readmission,
    ROUND(AVG(days_to_readmission), 2) AS mean_days_to_readmission
FROM final_analysis_dataset;

CREATE OR REPLACE VIEW validation_outpatient_followup_timing AS
SELECT
    COUNT(*) AS final_rows,
    SUM(outpatient_followup_7d) AS outpatient_followup_7d_count,
    SUM(outpatient_followup_14d) AS outpatient_followup_14d_count,
    SUM(outpatient_followup_30d) AS outpatient_followup_30d_count,
    SUM(
        CASE
            WHEN outpatient_followup_7d > outpatient_followup_14d
              OR outpatient_followup_14d > outpatient_followup_30d
            THEN 1 ELSE 0
        END
    ) AS non_monotonic_followup_window_rows,
    SUM(CASE WHEN days_to_first_outpatient_followup < 0 THEN 1 ELSE 0 END)
        AS negative_days_to_first_followup_rows,
    SUM(CASE WHEN days_to_first_outpatient_followup > 30 THEN 1 ELSE 0 END)
        AS over_30_day_first_followup_rows,
    SUM(CASE WHEN outpatient_followup_30d = 1 AND days_to_first_outpatient_followup IS NULL THEN 1 ELSE 0 END)
        AS followup_flag_missing_timing_rows,
    MIN(days_to_first_outpatient_followup) AS min_days_to_first_followup,
    MAX(days_to_first_outpatient_followup) AS max_days_to_first_followup,
    ROUND(AVG(days_to_first_outpatient_followup), 2) AS mean_days_to_first_followup
FROM final_analysis_dataset;

COPY validation_cohort_attrition_counts
TO 'outputs/validation/cohort_attrition_counts.csv'
WITH (HEADER, DELIMITER ',');

COPY validation_index_encounter_check
TO 'outputs/validation/index_encounter_check.csv'
WITH (HEADER, DELIMITER ',');

COPY validation_date_validity_checks
TO 'outputs/validation/date_validity_checks.csv'
WITH (HEADER, DELIMITER ',');

COPY validation_encounter_class_distribution
TO 'outputs/validation/encounter_class_distribution.csv'
WITH (HEADER, DELIMITER ',');

COPY validation_missingness_report
TO 'outputs/validation/missingness_report.csv'
WITH (HEADER, DELIMITER ',');

COPY validation_readmission_timing
TO 'outputs/validation/readmission_timing_validation.csv'
WITH (HEADER, DELIMITER ',');

COPY validation_outpatient_followup_timing
TO 'outputs/validation/outpatient_followup_timing_validation.csv'
WITH (HEADER, DELIMITER ',');
