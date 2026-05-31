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

## Sensitivity Analyses to Add Next

The most useful next analyses would not be more complex modeling first. They would be sensitivity analyses that test whether findings change under reasonable cohort and timing assumptions:

- Compare models using outpatient follow-up windows of 7, 14, and 30 days.
- Fit one model with outpatient follow-up excluded and one model with outpatient follow-up included because of timing bias concerns.
- Stratify summaries by prior utilization burden, such as prior ED use or high prior encounter count.
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
