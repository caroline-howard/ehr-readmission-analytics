-- Derive all-cause 30-day inpatient readmission after index discharge.
-- ED-only revisits are not counted as readmissions.

CREATE OR REPLACE VIEW readmission_outcomes AS
WITH typed_encounters AS (
    SELECT
        id AS encounter_id,
        patient AS patient_id,
        LOWER(encounterclass) AS encounter_class,
        TRY_CAST(start AS TIMESTAMP) AS encounter_start,
        TRY_CAST(stop AS TIMESTAMP) AS encounter_stop
    FROM raw_encounters
),
candidate_readmissions AS (
    SELECT
        i.patient_id,
        i.index_encounter_id,
        e.encounter_id AS readmission_encounter_id,
        e.encounter_start AS readmission_start,
        e.encounter_stop AS readmission_stop,
        DATE_DIFF('second', i.index_encounter_stop, e.encounter_start) / 86400.0
            AS days_to_readmission,
        CASE
            WHEN e.encounter_start <= i.index_encounter_stop + INTERVAL '1 day'
            THEN 1 ELSE 0
        END AS possible_same_day_transfer_flag,
        ROW_NUMBER() OVER (
            PARTITION BY i.patient_id, i.index_encounter_id
            ORDER BY e.encounter_start, e.encounter_stop, e.encounter_id
        ) AS readmission_rank
    FROM index_encounter i
    INNER JOIN typed_encounters e
        ON i.patient_id = e.patient_id
       AND e.encounter_id <> i.index_encounter_id
       AND e.encounter_class = 'inpatient'
       AND e.encounter_start > i.index_encounter_stop
       AND e.encounter_start <= i.index_encounter_stop + INTERVAL '30 days'
)
SELECT
    i.patient_id,
    i.index_encounter_id,
    CASE WHEN r.readmission_encounter_id IS NOT NULL THEN 1 ELSE 0 END AS readmitted_30d,
    r.readmission_encounter_id,
    r.readmission_start,
    r.readmission_stop,
    r.days_to_readmission,
    COALESCE(r.possible_same_day_transfer_flag, 0) AS possible_same_day_transfer_flag
FROM index_encounter i
LEFT JOIN candidate_readmissions r
    ON i.patient_id = r.patient_id
   AND i.index_encounter_id = r.index_encounter_id
   AND r.readmission_rank = 1;

-- Validation checks for the readmission outcome.
SELECT
    COUNT(*) AS index_rows,
    SUM(readmitted_30d) AS readmitted_30d_count,
    SUM(possible_same_day_transfer_flag) AS possible_same_day_transfer_count,
    SUM(CASE WHEN days_to_readmission < 0 THEN 1 ELSE 0 END) AS negative_readmission_timing_rows,
    SUM(CASE WHEN days_to_readmission > 30 THEN 1 ELSE 0 END) AS over_30_day_readmission_rows
FROM readmission_outcomes;
