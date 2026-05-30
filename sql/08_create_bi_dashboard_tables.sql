-- Create Power BI/Tableau-ready aggregate dashboard tables.
-- Requires sql/01 through sql/06 to be run first in the same DuckDB database.
-- These outputs support portfolio dashboard development and do not include
-- patient-level rows.

CREATE OR REPLACE TEMP TABLE bi_final_analysis AS
SELECT *
FROM final_analysis_dataset;

CREATE OR REPLACE VIEW bi_cohort_summary AS
SELECT
    COUNT(*) AS cohort_patients,
    ROUND(AVG(age_at_index), 1) AS mean_age_at_index,
    ROUND(MEDIAN(age_at_index), 1) AS median_age_at_index,
    SUM(age_group_65plus) AS patients_age_65plus,
    ROUND(100.0 * SUM(age_group_65plus) / NULLIF(COUNT(*), 0), 1)
        AS percent_age_65plus,
    ROUND(AVG(length_of_stay_days), 2) AS mean_length_of_stay_days,
    ROUND(MEDIAN(length_of_stay_days), 2) AS median_length_of_stay_days,
    ROUND(AVG(prior_encounters_12mo), 2) AS mean_prior_encounters_12mo,
    ROUND(AVG(chronic_condition_count), 2) AS mean_chronic_condition_count
FROM bi_final_analysis;

CREATE OR REPLACE VIEW bi_readmission_kpis AS
SELECT
    COUNT(*) AS cohort_patients,
    SUM(readmitted_30d) AS readmitted_30d_count,
    ROUND(100.0 * SUM(readmitted_30d) / NULLIF(COUNT(*), 0), 1)
        AS readmission_rate_30d_percent,
    ROUND(AVG(days_to_readmission), 2) AS mean_days_to_readmission,
    ROUND(MEDIAN(days_to_readmission), 2) AS median_days_to_readmission,
    MIN(days_to_readmission) AS min_days_to_readmission,
    MAX(days_to_readmission) AS max_days_to_readmission,
    SUM(possible_same_day_transfer_flag) AS possible_same_day_transfer_count,
    SUM(readmission_before_outpatient_followup_flag)
        AS readmission_before_outpatient_followup_count
FROM bi_final_analysis;

CREATE OR REPLACE VIEW bi_followup_timing AS
SELECT
    '0-7 days' AS followup_window,
    7 AS followup_window_days,
    SUM(outpatient_followup_7d) AS followup_count,
    ROUND(100.0 * SUM(outpatient_followup_7d) / NULLIF(COUNT(*), 0), 1)
        AS followup_percent,
    ROUND(AVG(CASE WHEN outpatient_followup_7d = 1 THEN days_to_first_outpatient_followup END), 2)
        AS mean_days_to_first_followup
FROM bi_final_analysis
UNION ALL
SELECT
    '0-14 days' AS followup_window,
    14 AS followup_window_days,
    SUM(outpatient_followup_14d) AS followup_count,
    ROUND(100.0 * SUM(outpatient_followup_14d) / NULLIF(COUNT(*), 0), 1)
        AS followup_percent,
    ROUND(AVG(CASE WHEN outpatient_followup_14d = 1 THEN days_to_first_outpatient_followup END), 2)
        AS mean_days_to_first_followup
FROM bi_final_analysis
UNION ALL
SELECT
    '0-30 days' AS followup_window,
    30 AS followup_window_days,
    SUM(outpatient_followup_30d) AS followup_count,
    ROUND(100.0 * SUM(outpatient_followup_30d) / NULLIF(COUNT(*), 0), 1)
        AS followup_percent,
    ROUND(AVG(CASE WHEN outpatient_followup_30d = 1 THEN days_to_first_outpatient_followup END), 2)
        AS mean_days_to_first_followup
FROM bi_final_analysis
ORDER BY followup_window_days;

CREATE OR REPLACE VIEW bi_ed_revisit_summary AS
SELECT
    COUNT(*) AS cohort_patients,
    SUM(ed_revisit_30d) AS ed_revisit_30d_count,
    ROUND(100.0 * SUM(ed_revisit_30d) / NULLIF(COUNT(*), 0), 1)
        AS ed_revisit_30d_percent,
    ROUND(AVG(total_postdischarge_encounters_30d), 2)
        AS mean_total_postdischarge_encounters_30d,
    SUM(CASE WHEN total_postdischarge_encounters_30d > 0 THEN 1 ELSE 0 END)
        AS any_postdischarge_encounter_30d_count,
    ROUND(
        100.0 * SUM(CASE WHEN total_postdischarge_encounters_30d > 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        1
    ) AS any_postdischarge_encounter_30d_percent
FROM bi_final_analysis;

CREATE OR REPLACE VIEW bi_demographic_utilization_summary AS
WITH long_summary AS (
    SELECT
        'sex' AS summary_domain,
        COALESCE(sex, 'Missing') AS category,
        COUNT(*) AS patient_count,
        SUM(readmitted_30d) AS readmitted_30d_count,
        SUM(outpatient_followup_30d) AS outpatient_followup_30d_count,
        SUM(ed_revisit_30d) AS ed_revisit_30d_count,
        ROUND(AVG(length_of_stay_days), 2) AS mean_length_of_stay_days,
        ROUND(AVG(prior_encounters_12mo), 2) AS mean_prior_encounters_12mo,
        ROUND(AVG(chronic_condition_count), 2) AS mean_chronic_condition_count
    FROM bi_final_analysis
    GROUP BY COALESCE(sex, 'Missing')
    UNION ALL
    SELECT
        'race' AS summary_domain,
        COALESCE(race, 'Missing') AS category,
        COUNT(*) AS patient_count,
        SUM(readmitted_30d) AS readmitted_30d_count,
        SUM(outpatient_followup_30d) AS outpatient_followup_30d_count,
        SUM(ed_revisit_30d) AS ed_revisit_30d_count,
        ROUND(AVG(length_of_stay_days), 2) AS mean_length_of_stay_days,
        ROUND(AVG(prior_encounters_12mo), 2) AS mean_prior_encounters_12mo,
        ROUND(AVG(chronic_condition_count), 2) AS mean_chronic_condition_count
    FROM bi_final_analysis
    GROUP BY COALESCE(race, 'Missing')
    UNION ALL
    SELECT
        'ethnicity' AS summary_domain,
        COALESCE(ethnicity, 'Missing') AS category,
        COUNT(*) AS patient_count,
        SUM(readmitted_30d) AS readmitted_30d_count,
        SUM(outpatient_followup_30d) AS outpatient_followup_30d_count,
        SUM(ed_revisit_30d) AS ed_revisit_30d_count,
        ROUND(AVG(length_of_stay_days), 2) AS mean_length_of_stay_days,
        ROUND(AVG(prior_encounters_12mo), 2) AS mean_prior_encounters_12mo,
        ROUND(AVG(chronic_condition_count), 2) AS mean_chronic_condition_count
    FROM bi_final_analysis
    GROUP BY COALESCE(ethnicity, 'Missing')
    UNION ALL
    SELECT
        'age_group' AS summary_domain,
        CASE WHEN age_group_65plus = 1 THEN '65+' ELSE 'Under 65' END AS category,
        COUNT(*) AS patient_count,
        SUM(readmitted_30d) AS readmitted_30d_count,
        SUM(outpatient_followup_30d) AS outpatient_followup_30d_count,
        SUM(ed_revisit_30d) AS ed_revisit_30d_count,
        ROUND(AVG(length_of_stay_days), 2) AS mean_length_of_stay_days,
        ROUND(AVG(prior_encounters_12mo), 2) AS mean_prior_encounters_12mo,
        ROUND(AVG(chronic_condition_count), 2) AS mean_chronic_condition_count
    FROM bi_final_analysis
    GROUP BY CASE WHEN age_group_65plus = 1 THEN '65+' ELSE 'Under 65' END
    UNION ALL
    SELECT
        'chronic_condition_count' AS summary_domain,
        CAST(chronic_condition_count AS VARCHAR) AS category,
        COUNT(*) AS patient_count,
        SUM(readmitted_30d) AS readmitted_30d_count,
        SUM(outpatient_followup_30d) AS outpatient_followup_30d_count,
        SUM(ed_revisit_30d) AS ed_revisit_30d_count,
        ROUND(AVG(length_of_stay_days), 2) AS mean_length_of_stay_days,
        ROUND(AVG(prior_encounters_12mo), 2) AS mean_prior_encounters_12mo,
        ROUND(AVG(chronic_condition_count), 2) AS mean_chronic_condition_count
    FROM bi_final_analysis
    GROUP BY chronic_condition_count
)
SELECT
    summary_domain,
    category,
    patient_count,
    ROUND(100.0 * patient_count / NULLIF(SUM(patient_count) OVER (PARTITION BY summary_domain), 0), 1)
        AS patient_percent_within_domain,
    readmitted_30d_count,
    ROUND(100.0 * readmitted_30d_count / NULLIF(patient_count, 0), 1)
        AS readmission_rate_30d_percent,
    outpatient_followup_30d_count,
    ROUND(100.0 * outpatient_followup_30d_count / NULLIF(patient_count, 0), 1)
        AS outpatient_followup_30d_percent,
    ed_revisit_30d_count,
    ROUND(100.0 * ed_revisit_30d_count / NULLIF(patient_count, 0), 1)
        AS ed_revisit_30d_percent,
    mean_length_of_stay_days,
    mean_prior_encounters_12mo,
    mean_chronic_condition_count
FROM long_summary
ORDER BY summary_domain, category;

COPY bi_cohort_summary
TO 'outputs/bi/cohort_summary_table.csv'
WITH (HEADER, DELIMITER ',');

COPY bi_readmission_kpis
TO 'outputs/bi/readmission_kpi_table.csv'
WITH (HEADER, DELIMITER ',');

COPY bi_followup_timing
TO 'outputs/bi/followup_timing_table.csv'
WITH (HEADER, DELIMITER ',');

COPY bi_ed_revisit_summary
TO 'outputs/bi/ed_revisit_table.csv'
WITH (HEADER, DELIMITER ',');

COPY bi_demographic_utilization_summary
TO 'outputs/bi/demographic_utilization_summary_table.csv'
WITH (HEADER, DELIMITER ',');
