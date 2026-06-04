# Retrospective Post-Discharge Utilization Analytics Workflow

[Overview](#project-overview) | [Final Results](#final-results-summary) | [Research Question](#research-question) | [Workflow Design](#healthcare-analytics-workflow-design) | [Analytics Focus](#core-analytics-focus) | [Analytic Scope](#analytic-scope) | [Technical Environment](#technical-environment) | [Dashboard and BI](#dashboard-and-bi-layer) | [Subgroup Caution](#statistical-caution-for-subgroup-comparisons) | [Sensitivity](#sensitivity-and-stratified-analysis) | [Results](#results-overview) | [Analysis](#analysis-layer) | [Stakeholder Use](#stakeholder-use-case) | [Skills](#skills-demonstrated) | [Workflow Status](#workflow-status) | [Repository Structure](#repository-structure) | [Data Setup](#data-setup) | [Outputs](#current-outputs) | [Responsible Use](#responsible-use)

## Project Overview

This project demonstrates an end-to-end retrospective healthcare utilization analytics workflow using Synthea synthetic EHR data. It simulates a health system analytics request to define an adult inpatient cohort, track core post-discharge utilization measures, identify outpatient follow-up timing, and evaluate factors associated with 30-day inpatient readmission.

The project is built for healthcare analytics, clinical research analytics, and health system research data analyst roles where reproducibility, data governance, SQL logic, and clear communication are essential.

## Final Results Summary

This project is complete as a portfolio demonstration of a retrospective EHR analytics workflow using synthetic Synthea data. The final result is not a clinical finding; it is a documented analytics workflow showing cohort definition, QA, post-discharge utilization derivation, statistical analysis, sensitivity analysis, and stakeholder-facing interpretation.

| Result | Finding |
| --- | --- |
| Final analytic cohort | 255 adult patients with one first eligible inpatient encounter |
| 30-day inpatient readmission | 13 patients, 5.1% |
| Outpatient follow-up within 7 days | 23 patients, 9.0% |
| Outpatient follow-up within 14 days | 33 patients, 12.9% |
| Outpatient follow-up within 30 days | 55 patients, 21.6% |
| ED revisit within 30 days | 2 patients, 0.8% |
| Any post-discharge encounter within 30 days | 96 patients, 37.6% |

The clearest descriptive story is prior utilization. Patients with high prior encounter burden had a higher observed 30-day readmission rate than patients with low or medium prior utilization.

| Prior utilization group | Patients | Readmission rate | 30-day follow-up |
| --- | ---: | ---: | ---: |
| Low prior utilization, 0-1 encounters | 88 | 2.3% | 5.7% |
| Medium prior utilization, 2-4 encounters | 101 | 3.0% | 18.8% |
| High prior utilization, 5+ encounters | 66 | 12.1% | 47.0% |

Prior ED use also provided a practical operational stratification signal: patients with any prior ED use had a 14.0% observed readmission rate compared with 2.5% among patients with no prior ED use.

The honest interpretation is that prior utilization burden is the strongest stakeholder-facing signal in this synthetic cohort. Outpatient follow-up timing is reported as observed utilization only and is not interpreted causally.

## Research Question

Among adult patients with a first eligible acute inpatient hospitalization in Synthea synthetic EHR data, how are outpatient follow-up timing, demographic characteristics, clinical conditions, prior utilization, and discharge-related factors associated with all-cause inpatient readmission within 30 days of discharge?

## What This Project Demonstrates

This project demonstrates the practical workflow behind a retrospective EHR analytics request: profiling raw data extracts, validating encounter classifications, defining an eligible inpatient cohort, deriving post-discharge utilization measures, creating a 30-day readmission outcome, and preparing reproducible analysis-ready outputs.

## Healthcare Analytics Workflow Design

This project follows a validation-first analytics workflow common in healthcare operations, population health, and clinical research analytics. Raw synthetic EHR extracts are profiled before cohort construction so available tables, fields, encounter classes, date structures, and missingness patterns are understood before outcome derivation.

The workflow emphasizes validation of encounter classification, temporal sequencing, missingness, and operational edge cases before analysis. SQL and Python are used to support reproducible, auditable healthcare analytics workflows that can be reviewed by technical analysts, clinical stakeholders, and population health teams.

This project intentionally separates data profiling, cohort construction, outcome derivation, validation, statistical analysis, and reporting so each step can be reviewed and updated independently.

## Why This Project Matters

Health system research and population health teams need reproducible workflows for defining cohorts, deriving post-discharge outcomes, validating EHR data, assessing missingness, conducting statistical analysis, and preparing manuscript-ready outputs. This project is intended to demonstrate those skills in a public, privacy-preserving way using synthetic data.

## Core Analytics Focus

- Retrospective EHR analytics
- Inpatient cohort construction
- Post-discharge utilization tracking
- 30-day readmission derivation
- Temporal sequencing validation
- SQL and Python healthcare analytics workflows
- Data validation and QA workflows
- Healthcare analytics-oriented documentation

## Outcome and Utilization Measures

- 30-day inpatient readmission
- ED revisit within 30 days
- Outpatient follow-up within 7, 14, and 30 days
- Days to first outpatient follow-up
- Total post-discharge encounters within 30 days

## Analytic Scope

The project is framed around post-discharge utilization analytics rather than generic readmission prediction. The core workflow focuses on defining an adult inpatient cohort, validating encounter and date logic, deriving outpatient follow-up timing, identifying ED revisits, and measuring all-cause 30-day inpatient readmission.

The completed portfolio version uses a focused MVP variable set: demographics, index hospitalization dates, length of stay, prior utilization, outpatient follow-up within 7, 14, and 30 days, ED revisit within 30 days when identifiable, and 30-day inpatient readmission. Additional variables such as disease subgroups, discharge disposition, payer, mortality, medication counts, and lab values are documented as exploratory extensions rather than required scope.

Outpatient follow-up measures are interpreted as observational utilization measures. This project does not claim that outpatient follow-up causes a change in readmission risk.

## Technical Environment

- SQL
- Python / pandas
- Jupyter notebooks
- Synthea synthetic EHR data
- Power BI or Tableau
- GitHub workflow with feature branching and pull requests

## Dashboard and BI Layer

The project also incorporates a healthcare operations and population health dashboard layer intended to simulate stakeholder-facing KPI reporting and utilization analytics workflows commonly used in health systems.

The BI layer is designed around readmission KPIs, follow-up analytics, ED revisit reporting, cohort summaries, and operational healthcare metrics. It is intended to support clear communication of cohort trends and post-discharge utilization patterns without presenting the project as a clinical decision tool. The repository includes dashboard-ready aggregate tables and a professional multi-panel summary visual for portfolio review.

Dashboard-ready aggregate tables are available in `outputs/bi/` and can be imported into Power BI or Tableau:

- `cohort_summary_table.csv`
- `readmission_kpi_table.csv`
- `followup_timing_table.csv`
- `ed_revisit_table.csv`
- `demographic_utilization_summary_table.csv`

Report-ready visuals are generated from aggregate synthetic-data outputs and are available in `outputs/figures/`. The root README intentionally emphasizes final results in text rather than relying on figures.

Selected visuals include cohort attrition, follow-up timing, prior utilization, and exploratory model summaries.

Tableau dashboard build materials are available in `tableau_dashboard/`. The package includes aggregate Tableau-ready CSVs, a reproducible export notebook, and a manual build guide. It does not represent a completed or published Tableau workbook.

Together, these materials support cohort attrition reporting, post-discharge utilization KPI reporting, follow-up timing visualization, prior utilization/readmission comparison, subgroup uncertainty review, and exploratory readmission modeling outputs.

## Statistical Caution for Subgroup Comparisons

Subgroup readmission rates in the Tableau exports are descriptive and exploratory. Wilson 95% confidence intervals are included for age-group and condition-group readmission rates to show uncertainty around small subgroup proportions.

The age-group comparison uses Fisher's exact test or chi-square testing where appropriate based on expected cell counts. Condition-group outputs include subgroup sample-size notes, and groups with fewer than 30 patients are flagged for cautious interpretation. These summaries use synthetic Synthea data, are not clinically representative, and should not be interpreted as causal or clinically validated findings.

Current subgroup outputs include:

- Age under 65: 5.8% readmission, Wilson 95% CI 3.3%-9.8%.
- Age 65+: 2.1% readmission, Wilson 95% CI 0.4%-11.1%.
- Age-group comparison: Fisher's exact test, p = 0.4726.
- Condition-group examples: COPD, chronic kidney disease, and diabetes are flagged as small subgroups because each has fewer than 30 patients.

## Sensitivity and Stratified Analysis

The completed analysis includes a sensitivity layer designed to make the project more useful for healthcare analytics and population health portfolio review. This layer focuses on practical utilization stratification and timing-aware model interpretation rather than adding complex models prematurely.

Key sensitivity outputs include:

- Prior utilization groups: low, medium, and high prior encounter burden.
- Prior ED use groups: no prior ED use versus any prior ED use in the 12 months before index hospitalization.
- Observed outpatient follow-up windows: 7-day, 14-day, and 30-day follow-up.
- Adjusted logistic regression comparisons with outpatient follow-up excluded and included as 7-day, 14-day, or 30-day covariates.

The strongest descriptive story remains prior utilization. In this synthetic cohort, readmission was 2.3% in the low prior-utilization group, 3.0% in the medium group, and 12.1% in the high group. Patients with any prior ED use had a 14.0% readmission rate compared with 2.5% among patients without prior ED use.

Observed outpatient follow-up increased from 9.0% within 7 days to 12.9% within 14 days and 21.6% within 30 days. These are utilization patterns only. The project does not claim that outpatient follow-up prevents readmission.

Model sensitivity results show why timing-aware interpretation matters. The no-follow-up model converged, while the 7-day follow-up model was not estimable because no readmissions occurred among patients with 7-day follow-up in this synthetic cohort. This is documented as an analytic caution rather than treated as a stable effect estimate.

## Results Overview

The workflow completed data profiling, SQL cohort construction, validation QA, aggregate BI output generation, descriptive analysis, sensitivity analysis, and exploratory modeling using local Synthea synthetic CSV data. These results are included to demonstrate reproducible healthcare analytics workflow design, not clinical performance or causal inference.

The final analytic dataset includes 255 adult patients with a first eligible inpatient encounter. Validation outputs confirmed one index encounter per patient, no missing primary readmission outcome, and no invalid index encounter start or stop dates in the final analytic dataset.

All-cause inpatient readmission within 30 days occurred for 13 patients, or 5.1% of the cohort. Outpatient follow-up was observed for 9.0% of patients within 7 days, 12.9% within 14 days, and 21.6% within 30 days. ED revisit within 30 days was uncommon in this synthetic cohort at 0.8%, while any post-discharge encounter within 30 days occurred for 37.6% of patients.

The most useful takeaway is operational: the workflow shows how a healthcare analyst can validate EHR-style encounter data, define post-discharge timing windows, produce aggregate utilization measures, stratify patients by prior utilization burden, and prepare a stakeholder-facing readout. The exploratory logistic regression included 255 observations and 13 readmission events and should be interpreted only as a demonstration of analytic workflow mechanics.

The full report is available in `report/final_report.md`.

## Analysis Layer

The analysis layer includes more than dashboard-level summary statistics. Current aggregate outputs include Table 1 baseline comparisons, post-discharge utilization summaries, risk stratification summaries, and an exploratory adjusted logistic regression model.

The analytic story is that the workflow can move from raw EHR-style extracts to a validated cohort, compare baseline characteristics by readmission status, evaluate post-discharge timing windows, stratify utilization patterns by patient groups, compare timing-sensitive model specifications, and translate findings into stakeholder questions.

The clearest descriptive signal in the current synthetic cohort is prior utilization:

- Prior encounters in the 12 months before index admission were higher among readmitted patients: 4.92 versus 3.66 encounters, p = 0.0405.
- Prior ED visits in the 12 months before index admission were higher among readmitted patients: 0.69 versus 0.24 visits, p = 0.0005.
- Outpatient follow-up within 30 days was similar between groups: 23.1% among readmitted patients versus 21.5% among non-readmitted patients.
- ED revisit within 30 days was rare overall and should not be overinterpreted.

Risk stratification outputs summarize readmission and utilization patterns by age group, chronic condition burden, and sex. These outputs are meant to show how a healthcare analyst would identify candidate subgroups for stakeholder review. Several strata have small cell counts, so the results should be used to generate questions rather than stable clinical risk estimates.

Logistic regression remains appropriate for an interpretable adjusted association analysis because the outcome is binary and odds ratios are common in healthcare research reporting. However, the model is intentionally framed as exploratory because the synthetic cohort has only 13 readmission events. In the current model, log length of stay was associated with higher odds of 30-day readmission, while age, sex, prior encounters, chronic condition count, and outpatient follow-up within 30 days did not show clear adjusted associations.

A real health system analysis with low event counts would consider penalized logistic regression, Firth-style rare-events logistic regression, or a prespecified parsimonious model before any prediction-focused machine learning. More complex machine learning would only be appropriate if the objective changed from explanatory healthcare analytics to validated prediction with enough data for training, testing, calibration, and performance reporting.

Sensitivity outputs now test the core utilization and timing assumptions:

- High prior-utilization patients had a higher observed readmission rate than low or medium prior-utilization patients.
- Patients with any prior ED use had a higher observed readmission rate than patients with no prior ED use.
- Follow-up window summaries compare 7-day, 14-day, and 30-day observed outpatient follow-up patterns.
- Model comparisons are reported with and without follow-up variables because follow-up timing can introduce bias in retrospective EHR analysis.
- The 7-day follow-up model is flagged as unstable because it did not converge cleanly in this small synthetic cohort.

## Stakeholder Use Case

A physician investigator, care transitions leader, quality improvement team, or population health analytics group could use this type of readout to move from raw encounter data toward operational questions about post-discharge care.

The current outputs would support discussion of outpatient follow-up access, high-utilization patients, encounter classification quality, timing-window validation, subgroup reporting, and whether the cohort definition matches the intended operational question. These outputs should be used to frame stakeholder review and next analytic questions, not to make clinical claims from synthetic data.

## Skills Demonstrated

- Healthcare analytics
- Population health analytics
- Healthcare operations analytics
- Retrospective clinical research
- Synthetic EHR data
- SQL cohort definition
- 30-day readmission outcome derivation
- Post-discharge outpatient follow-up measures
- ED revisit utilization measures
- Data validation and QA
- Missingness assessment
- BI/dashboard reporting workflows
- Report-ready aggregate tables and figures
- Table 1 descriptive analysis
- Sensitivity analysis and stratified utilization summaries
- Exploratory logistic regression
- Tableau-ready dashboard export package
- Mock IRB/data governance documentation
- Lightweight Gradio portfolio demo app

## Workflow Status

The current repository includes documentation, Synthea data profiling, SQL cohort construction, post-discharge utilization derivation, 30-day readmission logic, validation QA outputs, BI-ready aggregate tables, descriptive analysis notebooks, sensitivity analysis outputs, exploratory logistic regression, report materials, Tableau-ready exports, and a lightweight Gradio portfolio demo.

This project is ready to serve as a portfolio example of retrospective healthcare analytics workflow design. Future refinements could focus on dashboard design polish or additional edge-case sensitivity checks, but the core analysis and documentation are complete.

## Repository Structure

```text
docs/       Project overview, analytic plan, data dictionary, mock IRB summary, and limitations
data/       Local raw and processed Synthea data folders excluded from version control
sql/        SQL scripts for cohort construction, outcome derivation, and validation
notebooks/  Notebook-based data profiling, analysis, modeling, and output generation
outputs/    Generated tables, figures, and QA artifacts
report/     Manuscript-style report materials and final written outputs
app/        Gradio app for presenting project context and selected outputs
scripts/    Command-line utilities for local data profiling and reproducible workflows
```

## Data Source

This project will use synthetic EHR data generated by Synthea. Synthea creates realistic but artificial patient records for testing, education, and demonstration.

This repository will not contain real patient data. It will also avoid committing large synthetic data files, local databases, or generated artifacts unless they are intentionally small and appropriate for portfolio review.

## Data Setup

This project uses Synthea synthetic CSV data. Raw CSV files should be placed locally in `data/raw/`.

The `data/raw/` and `data/processed/` folders are intentionally empty on GitHub except for `.gitkeep` files. Raw data is not committed to GitHub. Processed data, local databases, and generated profiling outputs are also excluded from version control unless a small aggregate artifact is intentionally added for portfolio review.

Before cohort construction, run one of the profiling workflows:

- `notebooks/01_synthea_data_profile.ipynb`
- `scripts/profile_synthea_data.py`

The profiling step checks which Synthea tables are available, reviews table shapes and columns, summarizes encounter class/type values, and assesses date fields and missingness before cohort SQL is run or refreshed.

The current profiling review is documented in `docs/06_synthea_profile_review.md`.

Small aggregate validation and BI outputs are committed under `outputs/validation/` and `outputs/bi/` so reviewers can see the QA and dashboard layers without downloading raw data.

Detailed reproduction steps are available in `docs/07_reproducibility_guide.md`.

## Current Outputs

- Source table profile review
- SQL cohort construction scripts
- Cohort attrition table
- Missingness report
- Readmission timing validation
- Outpatient follow-up timing validation
- Encounter class distribution
- BI-ready cohort summary table
- BI-ready readmission KPI table
- BI-ready follow-up timing table
- BI-ready ED revisit table
- BI-ready demographic/utilization summary table
- Table 1 baseline characteristics
- Readmission, outpatient follow-up, and ED revisit summary tables
- Risk stratification summary
- Prior utilization and prior ED use stratification summaries
- Follow-up window sensitivity summary
- Model comparison sensitivity outputs
- Exploratory logistic regression results
- Analysis interpretation document
- Report-ready figures
- Current report summary
- Professional multi-panel utilization summary visual
- Lightweight Gradio demo app
- Reproducibility guide

Future milestones may add expanded dashboard views, refined visuals, or additional edge-case sensitivity checks after the current SQL/QA/BI, analysis, report, and app layers are reviewed.

## Portfolio Materials

- Final report: `report/final_report.md`
- Gradio demo app: `app/app.py`
- Reproducibility guide: `docs/07_reproducibility_guide.md`
- Analysis interpretation: `docs/09_analysis_interpretation.md`

## Responsible Use

This project is educational and portfolio-focused. It uses synthetic data only and does not include real patient data. It is not intended for clinical decision-making, patient risk prediction, quality reporting, or operational deployment.

Analyses from this project should be interpreted as synthetic-data demonstrations of workflow design. The project does not make causal claims about outpatient follow-up, readmission, ED revisits, or any clinical outcome.
