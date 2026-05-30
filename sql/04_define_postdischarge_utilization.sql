-- Derive post-discharge utilization measures after the index hospitalization.
-- Outpatient follow-up uses outpatient and ambulatory encounter classes.
-- ED revisits use emergency encounter class and remain distinct from readmission.

CREATE OR REPLACE VIEW postdischarge_utilization AS
WITH typed_encounters AS (
    SELECT
        id AS encounter_id,
        patient AS patient_id,
        LOWER(encounterclass) AS encounter_class,
        TRY_CAST(start AS TIMESTAMP) AS encounter_start,
        TRY_CAST(stop AS TIMESTAMP) AS encounter_stop
    FROM raw_encounters
),
postdischarge_encounters AS (
    SELECT
        i.patient_id,
        i.index_encounter_id,
        e.encounter_id,
        e.encounter_class,
        e.encounter_start,
        e.encounter_stop,
        DATE_DIFF('second', i.index_encounter_stop, e.encounter_start) / 86400.0
            AS days_after_discharge
    FROM index_encounter i
    INNER JOIN typed_encounters e
        ON i.patient_id = e.patient_id
       AND e.encounter_id <> i.index_encounter_id
       AND e.encounter_start > i.index_encounter_stop
       AND e.encounter_start <= i.index_encounter_stop + INTERVAL '30 days'
),
summarized AS (
    SELECT
        patient_id,
        index_encounter_id,
        MAX(
            CASE
                WHEN encounter_class IN ('outpatient', 'ambulatory')
                 AND days_after_discharge <= 7
                THEN 1 ELSE 0
            END
        ) AS outpatient_followup_7d,
        MAX(
            CASE
                WHEN encounter_class IN ('outpatient', 'ambulatory')
                 AND days_after_discharge <= 14
                THEN 1 ELSE 0
            END
        ) AS outpatient_followup_14d,
        MAX(
            CASE
                WHEN encounter_class IN ('outpatient', 'ambulatory')
                 AND days_after_discharge <= 30
                THEN 1 ELSE 0
            END
        ) AS outpatient_followup_30d,
        MIN(
            CASE
                WHEN encounter_class IN ('outpatient', 'ambulatory')
                THEN days_after_discharge
            END
        ) AS days_to_first_outpatient_followup,
        MAX(
            CASE
                WHEN encounter_class = 'emergency'
                 AND days_after_discharge <= 30
                THEN 1 ELSE 0
            END
        ) AS ed_revisit_30d,
        MIN(days_after_discharge) AS days_to_first_postdischarge_encounter,
        COUNT(*) AS total_postdischarge_encounters_30d
    FROM postdischarge_encounters
    GROUP BY patient_id, index_encounter_id
)
SELECT
    i.patient_id,
    i.index_encounter_id,
    COALESCE(s.outpatient_followup_7d, 0) AS outpatient_followup_7d,
    COALESCE(s.outpatient_followup_14d, 0) AS outpatient_followup_14d,
    COALESCE(s.outpatient_followup_30d, 0) AS outpatient_followup_30d,
    s.days_to_first_outpatient_followup,
    COALESCE(s.ed_revisit_30d, 0) AS ed_revisit_30d,
    s.days_to_first_postdischarge_encounter,
    COALESCE(s.total_postdischarge_encounters_30d, 0) AS total_postdischarge_encounters_30d
FROM index_encounter i
LEFT JOIN summarized s
    ON i.patient_id = s.patient_id
   AND i.index_encounter_id = s.index_encounter_id;

-- Validation checks for post-discharge utilization windows.
SELECT
    COUNT(*) AS index_rows,
    SUM(outpatient_followup_7d) AS outpatient_followup_7d_count,
    SUM(outpatient_followup_14d) AS outpatient_followup_14d_count,
    SUM(outpatient_followup_30d) AS outpatient_followup_30d_count,
    SUM(ed_revisit_30d) AS ed_revisit_30d_count,
    SUM(CASE WHEN days_to_first_outpatient_followup < 0 THEN 1 ELSE 0 END)
        AS negative_followup_timing_rows,
    SUM(CASE WHEN days_to_first_postdischarge_encounter < 0 THEN 1 ELSE 0 END)
        AS negative_postdischarge_timing_rows
FROM postdischarge_utilization;
