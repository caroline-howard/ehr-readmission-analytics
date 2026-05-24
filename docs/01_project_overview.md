# Project Overview

## Working Title

Retrospective EHR Analytics Workflow for 30-Day Readmission

## Scenario

A health system research or population health analytics team has been asked to support a physician investigator studying inpatient readmissions. The request is to build a reproducible retrospective EHR analytics workflow that defines an inpatient cohort, derives a 30-day readmission outcome, validates the analytic dataset, and prepares outputs suitable for research reporting.

This portfolio project simulates that request using Synthea synthetic EHR data so the workflow can be shared publicly without real patient information.

The documentation and planned variables are informed by examples from readmission research and CMS readmission reporting. Those sources highlight the importance of defining the index encounter, distinguishing inpatient readmissions from ED-only revisits, handling incomplete follow-up windows, and considering factors such as prior utilization, comorbidity burden, discharge setting, payer, race, and ethnicity.

## What This Project Demonstrates

The project demonstrates the practical analytics work behind a retrospective health system study:

- Translating a clinical analytics request into a cohort definition
- Building reproducible SQL logic for encounter selection and outcome derivation
- Validating patient, encounter, date, and outcome logic
- Translating literature-informed risk domains into variables supported by available EHR fields
- Assessing missingness and data quality issues
- Producing analysis-ready datasets for Python-based statistics
- Preparing manuscript-style tables, figures, and documentation

## Why a Healthcare Analytics Team Would Need This

Readmission analyses often require consistent definitions, transparent assumptions, and repeatable logic across data pulls. A healthcare analytics team needs a workflow that can be reviewed by investigators, adapted to available EHR fields, and audited when cohort counts or outcome rates change.

This project focuses on that workflow rather than on clinical deployment. It is intended to show the documentation, validation, and implementation thinking expected in healthcare analytics, clinical research analytics, and population health analytics roles.

## Source Materials Used for Design

The project design was informed by examples from readmission research and reporting, including:

- A CMS/NCQA report on readmissions reduction initiatives and vulnerable populations
- A retrospective EHR-based study of 30-day readmission after hypoglycemia-related emergency and inpatient encounters
- A retrospective study of 30-day readmission after acute inpatient cancer rehabilitation

These sources informed the planned attention to all-cause readmission definitions, prior utilization, discharge setting, comorbidity burden, equity-relevant characteristics, ED versus inpatient revisit distinctions, and follow-up window completeness. They do not provide results for this synthetic-data portfolio project.

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
