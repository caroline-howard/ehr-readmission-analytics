# Tableau Dashboard Build Guide

## Purpose

This guide supports manual Tableau dashboard development for the EHR Readmissions Analysis project. The dashboard should be presented as a portfolio-ready healthcare analytics mockup based on synthetic Synthea EHR data.

The repository does not include a completed or published Tableau workbook. These files are intended to help build the dashboard manually in Tableau Desktop or Tableau Public.

## Data Files

Use the aggregate CSV files in `tableau_dashboard/`:

| CSV file | Purpose |
| --- | --- |
| `kpi_summary.csv` | KPI cards for cohort size, readmission, follow-up, ED revisit, and any post-discharge encounter |
| `readmission_by_age_group.csv` | Age-group readmission and utilization summary |
| `readmission_by_condition_group.csv` | Condition-flag readmission summary using simplified Synthea condition groups |
| `utilization_summary.csv` | Post-discharge utilization measures and timing windows |
| `data_quality_summary.csv` | Data validation and missingness checks |
| `prior_utilization_stratification.csv` | Low, medium, and high prior encounter burden groups |
| `prior_ed_use_stratification.csv` | Any prior ED use versus no prior ED use |
| `followup_window_sensitivity.csv` | Observed 7-, 14-, and 30-day outpatient follow-up window comparison |
| `model_comparison_sensitivity.csv` | Adjusted model comparison with and without outpatient follow-up covariates |
| `model_without_followup_results.csv` | Baseline adjusted model coefficients without follow-up covariates |
| `model_with_followup_results.csv` | Adjusted model coefficients with 7-, 14-, and 30-day follow-up covariates |

Each file is aggregated and dashboard-friendly. Do not connect Tableau to raw patient-level files for this portfolio dashboard.

## Statistical Caution for Subgroup Comparisons

Subgroup rates are descriptive and exploratory. Wilson 95% confidence intervals are included to show uncertainty around readmission proportions, especially where subgroup counts are small.

The age-group comparison includes Fisher's exact or chi-square testing where appropriate based on expected cell counts. Condition-group outputs include sample-size notes and flag subgroups with fewer than 30 patients. These outputs use synthetic Synthea data, are not clinically representative, and should not be interpreted as causal or clinically validated findings.

Use neutral dashboard titles such as `Descriptive Readmission Rate by Age Group` or `Exploratory Condition-Group Readmission Summary`. Avoid titles that imply a causal effect, validated risk model, or production quality-reporting metric.

## Tableau Connections

1. Open Tableau Desktop or Tableau Public.
2. Connect to `Text file`.
3. Add each CSV from `tableau_dashboard/` as a separate data source.
4. Confirm field types:
   - Counts and denominators: Number whole
   - Percent fields: Number decimal
   - Category fields: String
   - Notes/status fields: String
5. Rename data sources in Tableau:
   - `KPI Summary`
   - `Readmission by Age Group`
   - `Readmission by Condition Group`
   - `Utilization Summary`
   - `Data Quality Summary`
   - `Prior Utilization Stratification`
   - `Prior ED Use Stratification`
   - `Follow-Up Window Sensitivity`
   - `Model Comparison Sensitivity`
   - `Model Without Follow-Up Results`
   - `Model With Follow-Up Results`

Do not join these files unless you intentionally need a combined worksheet. The package is designed so each sheet can use its own aggregate data source.

## Calculated Fields

Create these calculated fields in the relevant Tableau data sources. The CSVs already include percentage columns, but these formulas show transparent rate logic and make the workbook easier to audit.

### Readmission Rate

Use in `Readmission by Age Group` and `Readmission by Condition Group`.

```text
SUM([readmitted_30d_count]) / SUM([patient_count])
```

Format as Percentage with 1 decimal place.

### ED Revisit Rate

Use in `Readmission by Age Group`.

```text
SUM([ed_revisit_30d_count]) / SUM([patient_count])
```

Format as Percentage with 1 decimal place.

### Follow-Up Rate

Use in `Readmission by Age Group`.

```text
SUM([outpatient_followup_30d_count]) / SUM([patient_count])
```

Format as Percentage with 1 decimal place.

For `Utilization Summary`, use:

```text
SUM([count]) / SUM([denominator])
```

Format as Percentage with 1 decimal place.

### Percent Missing

Use in `Data Quality Summary`.

```text
SUM([value]) / SUM([denominator])
```

Format as Percentage with 1 decimal place.

## Recommended Dashboard Title

```text
Post-Discharge Utilization and 30-Day Readmission Dashboard
Synthetic Synthea EHR cohort | Aggregate portfolio dashboard | Not for clinical decision-making
```

## Sheet 1: KPI Cards

Data source: `KPI Summary`

Recommended chart type: Text cards

Build steps:

1. Create a new worksheet named `KPI Cards`.
2. Drag `kpi_name` to Columns.
3. Drag `display_value` to Text on the Marks card.
4. Drag `kpi_category` to Color.
5. Drag `count`, `denominator`, `percent`, and `interpretation_note` to Tooltip.
6. Set Marks type to Text.
7. Increase font size for `display_value`.
8. Hide field labels for columns.
9. Sort KPI cards manually in this order:
   - Final analytic cohort
   - 30-day inpatient readmission
   - 30-day outpatient follow-up
   - 30-day ED revisit
   - Any post-discharge encounter within 30 days

Suggested tooltip:

```text
<kpi_name>
Count: <count>
Denominator: <denominator>
Percent: <percent>%
Note: <interpretation_note>
```

## Sheet 2: Readmission Rate by Age Group

Data source: `Readmission by Age Group`

Recommended chart type: Bar chart

Build steps:

1. Create a worksheet named `Readmission Rate by Age Group`.
2. Drag `age_group` to Rows.
3. Drag `Readmission Rate` to Columns.
4. Drag `readmitted_30d_count` to Label.
5. Drag `patient_count` to Tooltip.
6. Drag `readmission_rate_ci_low_percent` and `readmission_rate_ci_high_percent` to Tooltip.
7. Drag `comparison_test`, `comparison_p_value`, and `comparison_interpretation` to Tooltip.
8. Drag `age_group` to Color or use one consistent healthcare-friendly color.
9. Drag `sort_order` to Sort so `Under 65` appears before `65+`.
10. Format `Readmission Rate` as Percentage with 1 decimal place.
11. Add a title: `Descriptive 30-Day Readmission Rate by Age Group`.

Suggested tooltip:

```text
Age group: <age_group>
Patients: <patient_count>
Readmitted: <readmitted_30d_count>
Readmission rate: <readmission_rate_30d_percent>%
95% CI: <readmission_rate_ci_low_percent>%–<readmission_rate_ci_high_percent>%
Comparison test: <comparison_test>
p-value: <comparison_p_value>
Note: <comparison_interpretation>
Outpatient follow-up rate: <Follow-Up Rate>
ED revisit rate: <ED Revisit Rate>
```

Interpretation note: age-group findings are descriptive and should be interpreted cautiously because readmission event counts are small.

## Sheet 3: Readmission Rate by Condition Group

Data source: `Readmission by Condition Group`

Recommended chart type: Horizontal bar chart

Build steps:

1. Create a worksheet named `Readmission Rate by Condition Group`.
2. Drag `condition_group` to Rows.
3. Drag `Readmission Rate` to Columns.
4. Drag `readmitted_30d_count` to Label.
5. Drag `patient_count`, `patient_percent`, `p_value`, and `interpretation_note` to Tooltip.
6. Drag `readmission_rate_ci_low_percent` and `readmission_rate_ci_high_percent` to Tooltip.
7. Drag `subgroup_sample_size_note` to Tooltip.
8. Sort descending by `Readmission Rate`.
9. Format `Readmission Rate` as Percentage with 1 decimal place.
10. Use a restrained palette, such as navy/teal with a muted accent color.
11. Add a title: `Exploratory Readmission Rate by Condition Group`.

Suggested tooltip:

```text
Condition group: <condition_group>
Patients with condition: <patient_count>
Readmitted: <readmitted_30d_count>
Readmission rate: <readmission_rate_30d_percent>%
95% CI: <readmission_rate_ci_low_percent>%–<readmission_rate_ci_high_percent>%
p-value from aggregate Table 1: <p_value>
Note: <subgroup_sample_size_note>
```

Interpretation note: condition groups are simplified Synthea flags and are not clinically validated disease phenotypes.

## Sheet 4: 30-Day ED Revisit vs Outpatient Follow-Up

Data source: `Utilization Summary`

Recommended chart type: Bar chart with filtered utilization measures

Build steps:

1. Create a worksheet named `30-Day ED Revisit vs Outpatient Follow-Up`.
2. Drag `measure_name` to Rows.
3. Drag `Follow-Up Rate` to Columns.
4. Drag `measure_group` to Color.
5. Drag `count` to Label.
6. Drag `denominator`, `percent`, `window_days`, and `interpretation_note` to Tooltip.
7. Add a filter on `measure_name`.
8. Select:
   - Outpatient follow-up 0-7 days
   - Outpatient follow-up 0-14 days
   - Outpatient follow-up 0-30 days
   - 30-day ED revisit
   - 30-day inpatient readmission
9. Format `Follow-Up Rate` as Percentage with 1 decimal place.
10. Add a title: `Post-Discharge Utilization Within 30 Days`.

Suggested tooltip:

```text
Measure: <measure_name>
Group: <measure_group>
Count: <count>
Denominator: <denominator>
Rate: <Follow-Up Rate>
Window: <window_days> days
Note: <interpretation_note>
```

Even though the calculated field is named `Follow-Up Rate`, it functions as a generic `count / denominator` rate in this utilization sheet.

## Sheet 5: Data Quality Summary

Data source: `Data Quality Summary`

Recommended chart type: Text table or highlight table

Build steps:

1. Create a worksheet named `Data Quality Summary`.
2. Drag `quality_domain` to Rows.
3. Drag `check_name` to Rows after `quality_domain`.
4. Drag `status` to Color.
5. Drag `value` to Text.
6. Drag `Percent Missing` to Tooltip.
7. Drag `denominator` and `interpretation_note` to Tooltip.
8. Use status colors:
   - Pass: muted green or teal
   - Expected: muted blue
   - Review: muted amber
9. Add a title: `Data Quality and Validation Checks`.

Suggested tooltip:

```text
Domain: <quality_domain>
Check: <check_name>
Value: <value>
Denominator: <denominator>
Percent: <Percent Missing>
Status: <status>
Note: <interpretation_note>
```

## Sheet 6: Readmission by Prior Utilization Group

Data source: `Prior Utilization Stratification`

Recommended chart type: Horizontal bar chart

Build steps:

1. Create a worksheet named `Readmission by Prior Utilization Group`.
2. Drag `prior_utilization_group` to Rows.
3. Drag `Readmission Rate` to Columns.
4. Drag `sort_order` to Sort so low, medium, and high groups appear in order.
5. Drag `readmitted_30d_count` to Label.
6. Drag `patient_count`, `not_readmitted_count`, `readmission_rate_ci_low_percent`, and `readmission_rate_ci_high_percent` to Tooltip.
7. Drag `outpatient_followup_30d_percent`, `ed_revisit_30d_percent`, `mean_prior_encounters_12mo`, and `interpretation_note` to Tooltip.
8. Use a muted red or burgundy accent for readmission rate bars.
9. Add a title: `Descriptive Readmission Rate by Prior Utilization Group`.

Suggested tooltip:

```text
Prior utilization group: <prior_utilization_group>
Patients: <patient_count>
Readmitted: <readmitted_30d_count>
Readmission rate: <readmission_rate_30d_percent>%
95% CI: <readmission_rate_ci_low_percent>%–<readmission_rate_ci_high_percent>%
30-day follow-up: <outpatient_followup_30d_percent>%
30-day ED revisit: <ed_revisit_30d_percent>%
Mean prior encounters: <mean_prior_encounters_12mo>
Note: <interpretation_note>
```

Interpretation note: this is the strongest descriptive dashboard story in the current synthetic cohort. Present it as prior utilization burden, not as a validated prediction score.

## Sheet 7: Readmission by Prior ED Use

Data source: `Prior ED Use Stratification`

Recommended chart type: Bar chart or side-by-side KPI comparison

Build steps:

1. Create a worksheet named `Readmission by Prior ED Use`.
2. Drag `prior_ed_use_group` to Rows.
3. Drag `Readmission Rate` to Columns.
4. Drag `sort_order` to Sort so `No prior ED use` appears before `Any prior ED use`.
5. Drag `readmitted_30d_count` to Label.
6. Drag `patient_count`, `readmission_rate_ci_low_percent`, `readmission_rate_ci_high_percent`, `outpatient_followup_30d_percent`, and `ed_revisit_30d_percent` to Tooltip.
7. Use color to distinguish the two groups, but keep the palette restrained.
8. Add a title: `Descriptive Readmission Rate by Prior ED Use`.

Suggested tooltip:

```text
Prior ED use group: <prior_ed_use_group>
Patients: <patient_count>
Readmitted: <readmitted_30d_count>
Readmission rate: <readmission_rate_30d_percent>%
95% CI: <readmission_rate_ci_low_percent>%–<readmission_rate_ci_high_percent>%
30-day follow-up: <outpatient_followup_30d_percent>%
30-day ED revisit: <ed_revisit_30d_percent>%
Note: <interpretation_note>
```

## Sheet 8: Follow-Up Window Sensitivity

Data source: `Follow-Up Window Sensitivity`

Recommended chart type: Line chart or bar chart

Build steps:

1. Create a worksheet named `Follow-Up Window Sensitivity`.
2. Drag `followup_window_days` to Columns.
3. Drag `followup_percent` to Rows.
4. Drag `followup_window` to Label or Detail.
5. Drag `followup_count`, `readmission_rate_with_followup_percent`, `readmission_rate_without_followup_percent`, and `interpretation_note` to Tooltip.
6. Format percent fields as percentages with 1 decimal place.
7. Add a title: `Observed Outpatient Follow-Up by Timing Window`.

Suggested tooltip:

```text
Window: <followup_window>
Patients with follow-up: <followup_count>
Follow-up percent: <followup_percent>%
Readmission rate with follow-up: <readmission_rate_with_followup_percent>%
Readmission rate without follow-up: <readmission_rate_without_followup_percent>%
Note: <interpretation_note>
```

Interpretation note: use language such as `observed follow-up patterns`; avoid language suggesting follow-up prevented readmission.

## Sheet 9: Model Sensitivity Summary

Data source: `Model Comparison Sensitivity`

Recommended chart type: Text table or compact bar chart

Build steps:

1. Create a worksheet named `Model Sensitivity Summary`.
2. Drag `model_name` to Rows.
3. Drag `aic`, `pseudo_r_squared`, and `llr_p_value` to Text or Measure Values.
4. Drag `converged` to Color.
5. Drag `readmission_events`, `n_observations`, `formatted_llr_p_value`, `interpretation_note`, and `comparison_note` to Tooltip.
6. Use a clear status color for convergence: muted teal for `True`, muted amber for `False`.
7. Add a title: `Adjusted Model Sensitivity to Follow-Up Timing Variables`.

Suggested tooltip:

```text
Model: <model_name>
Observations: <n_observations>
Readmission events: <readmission_events>
Converged: <converged>
Pseudo R-squared: <pseudo_r_squared>
AIC: <aic>
LLR p-value: <formatted_llr_p_value>
Note: <interpretation_note>
```

Interpretation note: the 7-day follow-up model did not converge cleanly in this synthetic cohort. Treat this as a sparse-data and timing-bias caution, not as a finding about follow-up effectiveness.

## Dashboard Wireframe

Recommended size: Automatic or 1400 x 900.

```text
+--------------------------------------------------------------------------------+
| Post-Discharge Utilization and 30-Day Readmission Dashboard                     |
| Synthetic Synthea EHR cohort | Aggregate portfolio dashboard | Not clinical CDS |
+--------------------------------------------------------------------------------+
| KPI Cards: Cohort | Readmission | Follow-Up | ED Revisit | Any Encounter       |
+------------------------------------------+-------------------------------------+
| Readmission Rate by Age Group            | Readmission Rate by Condition Group |
| Horizontal or vertical bar chart          | Horizontal bar chart                |
+------------------------------------------+-------------------------------------+
| Readmission by Prior Utilization Group   | Readmission by Prior ED Use         |
| Horizontal bar chart                      | Side-by-side bar or KPI comparison  |
+------------------------------------------+-------------------------------------+
| Follow-Up Window Sensitivity             | Model Sensitivity Summary           |
| Line/bar chart of observed windows        | Text table with convergence status  |
+--------------------------------------------------------------------------------+
| Data Quality Summary                                                            |
| Highlight table showing pass/expected/review validation checks                  |
+--------------------------------------------------------------------------------+
| Footer: Synthetic Synthea EHR data. Aggregate portfolio demonstration only.     |
| Not for clinical decision-making, quality reporting, or causal inference.       |
+--------------------------------------------------------------------------------+
```

## Dashboard Formatting Recommendations

- Use a restrained healthcare analytics palette: navy, teal, muted blue, muted red for readmission, and light gray backgrounds.
- Keep KPI cards at the top so reviewers immediately understand cohort size and core rates.
- Use concise titles and tooltips rather than long explanatory text inside the dashboard.
- Include a footer stating that the data are synthetic and not for clinical decision-making.
- Avoid patient-level detail tables.
- Avoid causal language about outpatient follow-up and readmission.

## Suggested Dashboard Story

The dashboard should communicate this flow:

1. The analytic cohort includes 255 adult synthetic patients with one first eligible inpatient encounter.
2. The primary outcome is all-cause 30-day inpatient readmission.
3. Post-discharge utilization includes outpatient follow-up windows, ED revisit, readmission, and any encounter within 30 days.
4. Prior utilization and prior ED use provide the clearest descriptive operational story in the current synthetic cohort.
5. Follow-up timing windows describe observed care patterns but do not imply causality.
6. Model sensitivity outputs show why timing variables and sparse events require caution.
7. Age and condition-group views are descriptive subgroup summaries.
8. Data quality checks support the cohort and outcome derivation logic but do not establish clinical validity.

## Responsible Use Language

Use this language in the dashboard footer or project notes:

```text
This dashboard uses synthetic Synthea EHR data for portfolio demonstration only. It does not contain real patient data and is not intended for clinical decision-making, quality reporting, operational deployment, or causal inference.
```
