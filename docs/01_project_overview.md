# Project Overview

## Working Title

Retrospective Post-Discharge Utilization Analytics Workflow

## Scenario

A physician investigator, quality improvement leader, or population health analytics team asks whether post-discharge follow-up patterns are associated with 30-day readmission in an adult inpatient population. This project demonstrates how I would translate that request into a reproducible SQL and Python analytics workflow.

The simulated request is: can we use EHR-style encounter data to define an inpatient cohort, track post-discharge utilization, identify outpatient follow-up timing, and evaluate factors associated with 30-day inpatient readmission?

This portfolio project uses Synthea synthetic EHR data so the workflow can be shared publicly without real patient information. The emphasis is on the analytic process a healthcare data analyst would need to demonstrate: cohort definition, time-window logic, data validation, reproducible analysis, and clear reporting.

## Research Question

Among adult patients with a first eligible acute inpatient hospitalization in Synthea synthetic EHR data, how are outpatient follow-up timing, demographic characteristics, clinical conditions, prior utilization, and discharge-related factors associated with all-cause inpatient readmission within 30 days of discharge?

## What This Project Demonstrates

The project demonstrates the practical analytics work behind a retrospective health system study:

- Translating a clinical analytics request into a cohort definition
- Building reproducible SQL logic for encounter selection and outcome derivation
- Validating patient, encounter, date, and outcome logic
- Translating literature-informed post-discharge utilization concepts into variables supported by available EHR fields
- Assessing missingness and data quality issues
- Producing analysis-ready datasets for Python-based statistics
- Preparing manuscript-style tables, figures, and documentation

## Why a Healthcare Analytics Team Would Need This

Post-discharge utilization analyses often require consistent definitions, transparent assumptions, and repeatable logic across data pulls. A healthcare analytics team needs a workflow that can distinguish inpatient readmissions from ED revisits and outpatient follow-up, adapt to available EHR fields, and be audited when cohort counts or outcome rates change.

This project focuses on that workflow rather than on clinical deployment. It is intended to show the documentation, validation, and implementation thinking expected in healthcare analytics, clinical research analytics, and population health analytics roles.

## Source Materials Used for Design

The project design was informed by health services research and readmission reporting examples, including:

- Balasubramanian et al. (2025), "Outpatient Follow-Up and 30-Day Readmissions: A Systematic Review and Meta-Analysis"
- A CMS/NCQA report on readmissions reduction initiatives and vulnerable populations
- A retrospective EHR-based study of 30-day readmission after hypoglycemia-related emergency and inpatient encounters
- A retrospective study of 30-day readmission after acute inpatient cancer rehabilitation

These sources informed the planned attention to outpatient follow-up timing, 7-day, 14-day, and 30-day windows, readmission and ED revisit distinctions, mortality flags when available, age and disease group stratification, prior utilization, comorbidity burden, and bias-aware interpretation. They do not provide results for this synthetic-data portfolio project.

## Planned Deliverables

- Project overview and operational analytic plan
- Draft data dictionary for planned analytic variables
- SQL scripts for cohort construction, outcome derivation, and validation
- Notebook-based descriptive and statistical analysis
- Cohort attrition, missingness, and validation summaries
- Manuscript-style tables and figures
- Lightweight Gradio app for portfolio presentation

## Out of Scope

- Real patient data
- Large synthetic data files committed to the repository
- Fake or placeholder results
- Clinical decision support
- Production deployment
