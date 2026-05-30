-- Define eligible adult inpatient encounters.
-- Requires sql/01_profile_source_tables.sql to create raw_* source views.

CREATE OR REPLACE VIEW eligible_inpatient_encounters AS
WITH typed_encounters AS (
    SELECT
        e.id AS encounter_id,
        e.patient AS patient_id,
        LOWER(e.encounterclass) AS encounter_class,
        e.code AS encounter_code,
        e.description AS encounter_description,
        TRY_CAST(e.start AS TIMESTAMP) AS encounter_start,
        TRY_CAST(e.stop AS TIMESTAMP) AS encounter_stop,
        e.organization,
        e.provider,
        e.payer
    FROM raw_encounters e
),
typed_patients AS (
    SELECT
        p.id AS patient_id,
        TRY_CAST(p.birthdate AS DATE) AS birth_date,
        TRY_CAST(p.deathdate AS DATE) AS death_date,
        p.gender AS sex,
        p.race,
        p.ethnicity
    FROM raw_patients p
),
eligible AS (
    SELECT
        e.encounter_id,
        e.patient_id,
        e.encounter_class,
        e.encounter_code,
        e.encounter_description,
        e.encounter_start,
        e.encounter_stop,
        p.birth_date,
        DATE_DIFF('year', p.birth_date, e.encounter_start) AS age_at_encounter,
        p.sex,
        p.race,
        p.ethnicity,
        p.death_date,
        e.organization,
        e.provider,
        e.payer,
        DATE_DIFF('second', e.encounter_start, e.encounter_stop) / 86400.0 AS length_of_stay_days
    FROM typed_encounters e
    INNER JOIN typed_patients p
        ON e.patient_id = p.patient_id
    WHERE e.encounter_class = 'inpatient'
      AND e.patient_id IS NOT NULL
      AND p.birth_date IS NOT NULL
      AND e.encounter_start IS NOT NULL
      AND e.encounter_stop IS NOT NULL
      AND e.encounter_stop >= e.encounter_start
      AND DATE_DIFF('year', p.birth_date, e.encounter_start) >= 18
)
SELECT *
FROM eligible;

-- Validation checks for the eligible inpatient encounter pool.
SELECT
    COUNT(*) AS eligible_inpatient_encounters,
    COUNT(DISTINCT patient_id) AS eligible_patients,
    SUM(CASE WHEN length_of_stay_days < 0 THEN 1 ELSE 0 END) AS negative_length_of_stay_rows,
    SUM(CASE WHEN age_at_encounter < 18 THEN 1 ELSE 0 END) AS under_18_rows,
    MIN(encounter_start) AS earliest_inpatient_start,
    MAX(encounter_stop) AS latest_inpatient_stop
FROM eligible_inpatient_encounters;
