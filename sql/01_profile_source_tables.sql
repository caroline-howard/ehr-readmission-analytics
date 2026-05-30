-- Profile local Synthea source tables before cohort construction.
-- DuckDB syntax. Run from the repository root so data/raw/*.csv paths resolve.
-- Raw CSV files are local only and should not be committed.

CREATE OR REPLACE VIEW raw_patients AS
SELECT
    "Id" AS id,
    "BIRTHDATE" AS birthdate,
    "DEATHDATE" AS deathdate,
    "SSN" AS ssn,
    "DRIVERS" AS drivers,
    "PASSPORT" AS passport,
    "PREFIX" AS prefix,
    "FIRST" AS first,
    "LAST" AS last,
    "SUFFIX" AS suffix,
    "MAIDEN" AS maiden,
    "MARITAL" AS marital,
    "RACE" AS race,
    "ETHNICITY" AS ethnicity,
    "GENDER" AS gender,
    "BIRTHPLACE" AS birthplace,
    "ADDRESS" AS address,
    "CITY" AS city,
    "STATE" AS state,
    "COUNTY" AS county,
    "ZIP" AS zip,
    "LAT" AS lat,
    "LON" AS lon,
    "HEALTHCARE_EXPENSES" AS healthcare_expenses,
    "HEALTHCARE_COVERAGE" AS healthcare_coverage
FROM read_csv_auto('data/raw/patients.csv');

CREATE OR REPLACE VIEW raw_encounters AS
SELECT
    "Id" AS id,
    "START" AS start,
    "STOP" AS stop,
    "PATIENT" AS patient,
    "ORGANIZATION" AS organization,
    "PROVIDER" AS provider,
    "PAYER" AS payer,
    "ENCOUNTERCLASS" AS encounterclass,
    "CODE" AS code,
    "DESCRIPTION" AS description,
    "BASE_ENCOUNTER_COST" AS base_encounter_cost,
    "TOTAL_CLAIM_COST" AS total_claim_cost,
    "PAYER_COVERAGE" AS payer_coverage,
    "REASONCODE" AS reasoncode,
    "REASONDESCRIPTION" AS reasondescription
FROM read_csv_auto('data/raw/encounters.csv');

CREATE OR REPLACE VIEW raw_conditions AS
SELECT
    "START" AS start,
    "STOP" AS stop,
    "PATIENT" AS patient,
    "ENCOUNTER" AS encounter,
    "CODE" AS code,
    "DESCRIPTION" AS description
FROM read_csv_auto('data/raw/conditions.csv');

-- Table-level row counts for MVP source tables.
SELECT 'patients' AS table_name, COUNT(*) AS row_count FROM raw_patients
UNION ALL
SELECT 'encounters' AS table_name, COUNT(*) AS row_count FROM raw_encounters
UNION ALL
SELECT 'conditions' AS table_name, COUNT(*) AS row_count FROM raw_conditions
ORDER BY table_name;

-- Encounter class review. This drives the inpatient, outpatient follow-up,
-- and ED revisit definitions in later scripts.
SELECT
    encounterclass,
    COUNT(*) AS encounter_count
FROM raw_encounters
GROUP BY encounterclass
ORDER BY encounter_count DESC;

-- Encounter date completeness and temporal validity.
SELECT
    COUNT(*) AS encounter_rows,
    SUM(CASE WHEN start IS NULL THEN 1 ELSE 0 END) AS missing_start,
    SUM(CASE WHEN stop IS NULL THEN 1 ELSE 0 END) AS missing_stop,
    SUM(CASE WHEN TRY_CAST(start AS TIMESTAMP) IS NULL THEN 1 ELSE 0 END) AS invalid_start_timestamp,
    SUM(CASE WHEN TRY_CAST(stop AS TIMESTAMP) IS NULL THEN 1 ELSE 0 END) AS invalid_stop_timestamp,
    SUM(
        CASE
            WHEN TRY_CAST(stop AS TIMESTAMP) < TRY_CAST(start AS TIMESTAMP)
            THEN 1 ELSE 0
        END
    ) AS stop_before_start
FROM raw_encounters;

-- Core identifier join checks.
SELECT
    (SELECT COUNT(*) FROM raw_encounters e LEFT JOIN raw_patients p ON e.patient = p.id WHERE p.id IS NULL)
        AS encounters_without_patient_match,
    (SELECT COUNT(*) FROM raw_conditions c LEFT JOIN raw_patients p ON c.patient = p.id WHERE p.id IS NULL)
        AS conditions_without_patient_match,
    (SELECT COUNT(*) FROM raw_conditions c LEFT JOIN raw_encounters e ON c.encounter = e.id WHERE e.id IS NULL)
        AS conditions_without_encounter_match,
    (SELECT COUNT(*) FROM (SELECT id FROM raw_patients GROUP BY id HAVING COUNT(*) > 1))
        AS duplicate_patient_ids,
    (SELECT COUNT(*) FROM (SELECT id FROM raw_encounters GROUP BY id HAVING COUNT(*) > 1))
        AS duplicate_encounter_ids;
