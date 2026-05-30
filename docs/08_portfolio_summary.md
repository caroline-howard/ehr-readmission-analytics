# Portfolio Summary

## Project Description

`ehr-readmission-analytics` is a synthetic EHR healthcare analytics portfolio project that demonstrates an end-to-end retrospective post-discharge utilization workflow. The project uses Synthea synthetic CSV data to define an adult inpatient cohort, derive outpatient follow-up timing, identify ED revisits, create a 30-day inpatient readmission outcome, validate temporal logic, generate BI-ready KPI tables, and fit an exploratory logistic regression model.

The project is designed for healthcare analytics, clinical research analytics, population health analytics, healthcare operations analytics, and health system research data analyst roles.

## Tools Used

- SQL and DuckDB for cohort construction and outcome derivation
- Python and pandas for profiling, descriptive analysis, and output generation
- Jupyter notebooks for reproducible analytics
- statsmodels for exploratory logistic regression
- matplotlib for report-ready figures and dashboard mockup
- Gradio for a lightweight portfolio demo app
- GitHub feature branches and pull requests for version-controlled workflow
- Synthea synthetic EHR data for privacy-preserving public demonstration

## Healthcare Analytics Skills Demonstrated

- Retrospective EHR cohort definition
- Inpatient encounter classification and index encounter selection
- 30-day readmission outcome derivation
- Outpatient follow-up timing windows
- ED revisit utilization measurement
- Data validation and QA checks
- Missingness assessment
- Table 1 baseline characteristics
- Exploratory logistic regression
- BI/dashboard-ready aggregate reporting
- Manuscript-style reporting and responsible-use documentation

## Resume Bullets

- Built an end-to-end retrospective EHR analytics workflow using Synthea synthetic data to define an adult inpatient cohort, derive 30-day readmission, and track post-discharge outpatient follow-up and ED revisit measures.
- Developed DuckDB SQL scripts for source profiling, cohort construction, index encounter selection, post-discharge utilization derivation, readmission outcome logic, validation QA, and BI-ready aggregate table generation.
- Created reproducible Python/Jupyter analysis notebooks for Table 1 baseline characteristics, readmission summaries, outpatient follow-up summaries, ED revisit summaries, and exploratory logistic regression.
- Produced healthcare operations dashboard-ready aggregate outputs and report-ready visuals for cohort attrition, utilization KPIs, encounter class distribution, and odds ratio reporting.
- Documented data governance, synthetic data limitations, reproducibility steps, and responsible-use constraints for a public healthcare analytics portfolio project.

## LinkedIn / Portfolio Blurb

I built a synthetic EHR post-discharge utilization analytics project to demonstrate the workflow behind retrospective healthcare analytics requests. Using Synthea data, SQL, Python, and Jupyter, the project defines an adult inpatient cohort, derives outpatient follow-up timing, ED revisit, and 30-day readmission measures, performs validation QA, creates dashboard-ready aggregate tables, and fits an exploratory logistic regression model. The repository emphasizes reproducibility, data governance, cohort logic, temporal validation, and healthcare analytics communication without using real patient data.

## Suggested Interview Framing

This project is not meant to prove clinical conclusions. It is meant to show how I would translate a health system analytics request into a reproducible workflow: understand the raw EHR-style extracts, validate encounter types and dates, define the cohort, derive outcomes and utilization measures, check edge cases, produce stakeholder-ready outputs, and communicate limitations clearly.
