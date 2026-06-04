# Analysis Interpretation

## Purpose

This document explains how the current descriptive, stratified, and exploratory regression outputs should be interpreted for a healthcare analytics portfolio audience. It is intended to make the analysis layer more explicit than a dashboard KPI summary.

The project uses Synthea synthetic EHR data. Findings are workflow demonstrations only and should not be treated as clinical evidence, quality benchmarks, or causal estimates.

## Analytic Story

The current analysis asks whether post-discharge utilization patterns and baseline patient characteristics differ by 30-day inpatient readmission status. The strongest analytic story is not that the model predicts readmission well. The stronger story is that the workflow can:

- define a reproducible inpatient cohort
- validate temporal logic before analysis
- compare baseline characteristics by readmission status
- summarize post-discharge utilization windows
- stratify readmission and follow-up patterns by patient groups
- fit an adjusted association model with appropriate limitations
- translate results into stakeholder questions for care transitions and population health teams

## Descriptive Signals

The Table 1 output suggests that prior utilization is the clearest signal in the current synthetic cohort:

- Prior encounters in the 12 months before index admission were higher among readmitted patients: 4.92 versus 3.66 encounters, p = 0.0405.
- Prior ED visits in the 12 months before index admission were higher among readmitted patients: 0.69 versus 0.24 visits, p = 0.0005.
- Outpatient follow-up within 30 days was similar between groups: 23.1% among readmitted patients versus 21.5% among non-readmitted patients.
- ED revisit within 30 days was rare overall and should not be overinterpreted.

These findings are most useful as stakeholder discussion points. In a real health system setting, they would support questions about whether prior ED use or broader prior utilization should be used for transition-of-care risk stratification.

## Prior Utilization Sensitivity Readout

The sensitivity analysis makes the prior-utilization story more explicit:

- Low prior utilization, defined as 0-1 prior encounters, included 88 patients and had a 2.3% observed readmission rate.
- Medium prior utilization, defined as 2-4 prior encounters, included 101 patients and had a 3.0% observed readmission rate.
- High prior utilization, defined as 5 or more prior encounters, included 66 patients and had a 12.1% observed readmission rate.
- Patients with any prior ED use had a 14.0% observed readmission rate compared with 2.5% among patients with no prior ED use.

This gives the Tableau dashboard a more coherent healthcare analytics story: prior utilization is a practical operational stratification variable that could help a care transitions or population health team decide where to focus review. The result is still synthetic and descriptive, not a validated risk score.

## Follow-Up Window Sensitivity

Observed outpatient follow-up increased across wider time windows:

- 9.0% of patients had outpatient follow-up within 7 days.
- 12.9% had outpatient follow-up within 14 days.
- 21.6% had outpatient follow-up within 30 days.

Readmission rates among patients with observed follow-up were 0.0% for the 7-day window, 9.1% for the 14-day window, and 5.5% for the 30-day window. These should be interpreted as observed utilization patterns only. They do not show whether follow-up prevents readmission because timing, baseline risk, illness severity, scheduling access, and early readmission can all affect whether follow-up is observed.

## Risk Stratification Readout

The risk stratification summary is based on aggregate outputs in `outputs/bi/demographic_utilization_summary_table.csv` and summarized in `outputs/analysis/risk_stratification_summary.csv`.

Current synthetic-data patterns include:

- Patients under 65 had a higher observed readmission rate than patients 65 and older in this synthetic cohort, but this should not be interpreted as a real-world age effect.
- Readmission rates varied across chronic condition count groups, but several strata have very small cell counts.
- Race and ethnicity strata are included for completeness and equity-aware analytics workflow design, but small groups should be interpreted cautiously.

The purpose of this stratification is to demonstrate how a healthcare analyst would identify candidate subgroups for stakeholder review, not to produce clinical conclusions.

## Modeling Interpretation

Logistic regression remains appropriate for the primary adjusted analysis because the outcome is binary and odds ratios are familiar in clinical research and healthcare analytics reporting. The model is intentionally parsimonious because the current synthetic cohort has only 13 readmission events.

The current exploratory logistic regression suggests:

- Log length of stay was associated with higher odds of 30-day readmission in the synthetic model: odds ratio 1.68, 95% CI 1.12-2.54, p = 0.0125.
- Age, sex, prior encounters, chronic condition count, and outpatient follow-up within 30 days did not show clear adjusted associations in the current synthetic model.
- The model should not be used as a clinical prediction tool because the event count is small and the data are synthetic.

In a real analysis with a larger governed dataset, the next modeling step would likely be a penalized logistic regression, Firth-style rare-events logistic regression, or a prespecified parsimonious model with validation. Machine learning methods would only be appropriate if the project objective changed from explanatory healthcare analytics to validated prediction.

## Model Sensitivity Interpretation

Adjusted model comparisons were added to test whether the model story changes when outpatient follow-up timing variables are included:

- The no-follow-up model converged and provides the cleanest baseline adjusted association model.
- The 7-day follow-up model did not converge cleanly because no readmissions occurred among patients with observed 7-day follow-up in this synthetic cohort.
- The 14-day and 30-day follow-up models converged, but results remain exploratory because there are only 13 readmission events.
- The model comparison is useful for demonstrating timing-bias awareness, not for claiming that follow-up changes readmission risk.

The most useful next analyses would review data-definition edge cases before adding more complex models:

- Review same-day returns and possible transfer-like encounters separately.
- Repeat descriptive summaries for age 65+ versus under 65.
- Consider excluding patients without complete 30-day follow-up if observation-window completeness can be measured.
- Add disease-specific cohorts only if condition grouping logic is defensible.

## Stakeholder Implications

For a care transitions, quality improvement, or population health analytics team, the current analysis would support questions such as:

- Should patients with prior ED use receive earlier discharge follow-up or outreach?
- Is outpatient follow-up being completed within 7 or 14 days for enough discharged patients?
- Are readmission, ED revisit, and outpatient follow-up definitions aligned with clinical and operational expectations?
- Would a disease-specific cohort produce more actionable findings than a broad all-cause inpatient cohort?
- Are additional data elements needed, such as discharge disposition, service line, post-acute placement, or scheduled follow-up orders?

The analytic value of the project is the reproducible chain from cohort definition through validation, stratified summaries, adjusted modeling, and stakeholder interpretation.
