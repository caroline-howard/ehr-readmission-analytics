# Project Overview

## Working Title

Retrospective EHR Analytics Workflow for 30-Day Readmission

## Scenario

A health system research or population health analytics team has been asked to support a physician investigator studying inpatient readmissions. The request is to build a reproducible retrospective EHR analytics workflow that defines an inpatient cohort, derives a 30-day readmission outcome, validates the analytic dataset, and prepares outputs suitable for research reporting.

This portfolio project simulates that request using Synthea synthetic EHR data so the workflow can be shared publicly without real patient information.

## What This Project Demonstrates

The project demonstrates the practical analytics work behind a retrospective health system study:

- Translating a clinical analytics request into a cohort definition
- Building reproducible SQL logic for encounter selection and outcome derivation
- Validating patient, encounter, date, and outcome logic
- Assessing missingness and data quality issues
- Producing analysis-ready datasets for Python-based statistics
- Preparing manuscript-style tables, figures, and documentation

## Why a Healthcare Analytics Team Would Need This

Readmission analyses often require consistent definitions, transparent assumptions, and repeatable logic across data pulls. A healthcare analytics team needs a workflow that can be reviewed by investigators, adapted to available EHR fields, and audited when cohort counts or outcome rates change.

This project focuses on that workflow rather than on clinical deployment. It is intended to show the documentation, validation, and implementation thinking expected in healthcare analytics, clinical research analytics, and population health analytics roles.

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
