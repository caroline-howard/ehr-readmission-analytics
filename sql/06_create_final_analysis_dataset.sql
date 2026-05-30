-- Create the MVP analysis-ready dataset for descriptive analysis and later modeling.
-- This is still a synthetic-data portfolio workflow, not a clinical tool.

CREATE OR REPLACE VIEW final_analysis_dataset AS
WITH prior_utilization AS (
    SELECT
        i.patient_id,
        i.index_encounter_id,
        COUNT(e.id) AS prior_encounters_12mo,
        SUM(CASE WHEN LOWER(e.encounterclass) = 'emergency' THEN 1 ELSE 0 END)
            AS prior_ed_visits_12mo,
        SUM(CASE WHEN LOWER(e.encounterclass) = 'inpatient' THEN 1 ELSE 0 END)
            AS prior_inpatient_12mo
    FROM index_encounter i
    LEFT JOIN raw_encounters e
        ON i.patient_id = e.patient
       AND TRY_CAST(e.start AS TIMESTAMP) < i.index_encounter_start
       AND TRY_CAST(e.start AS TIMESTAMP) >= i.index_encounter_start - INTERVAL '12 months'
    GROUP BY i.patient_id, i.index_encounter_id
),
condition_flags AS (
    SELECT
        i.patient_id,
        i.index_encounter_id,
        MAX(
            CASE
                WHEN REGEXP_MATCHES(LOWER(c.description), 'diabetes|diabetic')
                 AND NOT REGEXP_MATCHES(LOWER(c.description), 'prediabetes')
                THEN 1 ELSE 0
            END
        ) AS diabetes_flag,
        MAX(
            CASE
                WHEN REGEXP_MATCHES(LOWER(c.description), 'hypertension|hypertensive')
                THEN 1 ELSE 0
            END
        ) AS hypertension_flag,
        MAX(
            CASE
                WHEN REGEXP_MATCHES(LOWER(c.description), 'chronic kidney|kidney disease|renal disease|renal failure|diabetic renal')
                THEN 1 ELSE 0
            END
        ) AS ckd_flag,
        MAX(
            CASE
                WHEN REGEXP_MATCHES(LOWER(c.description), 'chronic obstructive|copd')
                THEN 1 ELSE 0
            END
        ) AS copd_flag
    FROM index_encounter i
    LEFT JOIN raw_conditions c
        ON i.patient_id = c.patient
       AND TRY_CAST(c.start AS DATE) <= CAST(i.index_encounter_stop AS DATE)
    GROUP BY i.patient_id, i.index_encounter_id
),
condition_summary AS (
    SELECT
        patient_id,
        index_encounter_id,
        COALESCE(diabetes_flag, 0) AS diabetes_flag,
        COALESCE(hypertension_flag, 0) AS hypertension_flag,
        COALESCE(ckd_flag, 0) AS ckd_flag,
        COALESCE(copd_flag, 0) AS copd_flag,
        COALESCE(diabetes_flag, 0)
            + COALESCE(hypertension_flag, 0)
            + COALESCE(ckd_flag, 0)
            + COALESCE(copd_flag, 0) AS chronic_condition_count
    FROM condition_flags
)
SELECT
    i.patient_id,
    i.index_encounter_id,
    i.birth_date,
    i.age_at_index,
    i.age_group_65plus,
    i.sex,
    i.race,
    i.ethnicity,
    i.index_encounter_start AS encounter_start,
    i.index_encounter_stop AS encounter_stop,
    i.length_of_stay_days,
    COALESCE(pu.prior_encounters_12mo, 0) AS prior_encounters_12mo,
    COALESCE(pu.prior_ed_visits_12mo, 0) AS prior_ed_visits_12mo,
    COALESCE(pu.prior_inpatient_12mo, 0) AS prior_inpatient_12mo,
    u.outpatient_followup_7d,
    u.outpatient_followup_14d,
    u.outpatient_followup_30d,
    u.days_to_first_outpatient_followup,
    u.ed_revisit_30d,
    u.days_to_first_postdischarge_encounter,
    u.total_postdischarge_encounters_30d,
    r.readmitted_30d,
    r.readmission_encounter_id,
    r.days_to_readmission,
    CASE
        WHEN r.readmitted_30d = 1
         AND u.days_to_first_outpatient_followup IS NOT NULL
         AND r.days_to_readmission < u.days_to_first_outpatient_followup
        THEN 1 ELSE 0
    END AS readmission_before_outpatient_followup_flag,
    r.possible_same_day_transfer_flag,
    c.diabetes_flag,
    c.hypertension_flag,
    c.ckd_flag,
    c.copd_flag,
    c.chronic_condition_count,
    i.death_date,
    CASE
        WHEN i.death_date BETWEEN CAST(i.index_encounter_start AS DATE)
                              AND CAST(i.index_encounter_stop AS DATE)
        THEN 1 ELSE 0
    END AS deceased_during_index,
    CASE
        WHEN i.death_date > CAST(i.index_encounter_stop AS DATE)
         AND i.death_date <= CAST(i.index_encounter_stop AS DATE) + INTERVAL '30 days'
        THEN 1 ELSE 0
    END AS postdischarge_death_30d,
    i.index_payer AS payer
FROM index_encounter i
LEFT JOIN prior_utilization pu
    ON i.patient_id = pu.patient_id
   AND i.index_encounter_id = pu.index_encounter_id
LEFT JOIN postdischarge_utilization u
    ON i.patient_id = u.patient_id
   AND i.index_encounter_id = u.index_encounter_id
LEFT JOIN readmission_outcomes r
    ON i.patient_id = r.patient_id
   AND i.index_encounter_id = r.index_encounter_id
LEFT JOIN condition_summary c
    ON i.patient_id = c.patient_id
   AND i.index_encounter_id = c.index_encounter_id;

-- Final dataset validation checks.
SELECT
    COUNT(*) AS final_rows,
    COUNT(DISTINCT patient_id) AS final_patients,
    COUNT(*) - COUNT(DISTINCT patient_id) AS duplicate_patient_rows,
    SUM(CASE WHEN patient_id IS NULL THEN 1 ELSE 0 END) AS missing_patient_id_rows,
    SUM(CASE WHEN index_encounter_id IS NULL THEN 1 ELSE 0 END) AS missing_index_encounter_id_rows,
    SUM(CASE WHEN readmitted_30d IS NULL THEN 1 ELSE 0 END) AS missing_readmission_outcome_rows,
    SUM(readmitted_30d) AS readmitted_30d_count,
    SUM(outpatient_followup_7d) AS outpatient_followup_7d_count,
    SUM(outpatient_followup_14d) AS outpatient_followup_14d_count,
    SUM(outpatient_followup_30d) AS outpatient_followup_30d_count,
    SUM(ed_revisit_30d) AS ed_revisit_30d_count,
    SUM(readmission_before_outpatient_followup_flag) AS readmission_before_followup_count
FROM final_analysis_dataset;
