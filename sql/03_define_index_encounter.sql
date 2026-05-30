-- Select one index hospitalization per eligible adult patient.
-- The first eligible inpatient encounter is used to reduce within-patient
-- correlation and keep the MVP cohort interpretable.

CREATE OR REPLACE VIEW index_encounter AS
WITH ranked_inpatient AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY patient_id
            ORDER BY encounter_start, encounter_stop, encounter_id
        ) AS inpatient_rank
    FROM eligible_inpatient_encounters
)
SELECT
    patient_id,
    encounter_id AS index_encounter_id,
    encounter_class AS index_encounter_class,
    encounter_code AS index_encounter_code,
    encounter_description AS index_encounter_description,
    encounter_start AS index_encounter_start,
    encounter_stop AS index_encounter_stop,
    birth_date,
    age_at_encounter AS age_at_index,
    CASE WHEN age_at_encounter >= 65 THEN 1 ELSE 0 END AS age_group_65plus,
    sex,
    race,
    ethnicity,
    death_date,
    organization AS index_organization,
    provider AS index_provider,
    payer AS index_payer,
    length_of_stay_days
FROM ranked_inpatient
WHERE inpatient_rank = 1;

-- Validation checks for one index encounter per patient.
SELECT
    COUNT(*) AS index_encounters,
    COUNT(DISTINCT patient_id) AS index_patients,
    COUNT(*) - COUNT(DISTINCT patient_id) AS duplicate_index_patient_rows,
    SUM(CASE WHEN age_at_index < 18 THEN 1 ELSE 0 END) AS under_18_index_rows,
    SUM(CASE WHEN length_of_stay_days < 0 THEN 1 ELSE 0 END) AS negative_los_rows,
    MIN(index_encounter_start) AS earliest_index_start,
    MAX(index_encounter_stop) AS latest_index_stop
FROM index_encounter;
