# Sparse-Event Modeling Check: Not for Clinical Interpretation

This archived note preserves the exploratory modeling content that was removed from the main Version 1 descriptive validation report. The model was run as a diagnostic check and demonstrates why the Version 1 cohort is not appropriate for clinical prediction or discharge-time risk stratification.

The final synthetic cohort included 255 observations and only 13 readmission events. That event count is too small for stable multivariable readmission modeling. Estimates should not be interpreted as clinical evidence, validated risk factors, or a usable predictive model.

## Exploratory Logistic Regression Diagnostic

An exploratory logistic regression model was fit for 30-day inpatient readmission using age, sex, log length of stay, prior encounters, chronic condition count, and outpatient follow-up within 30 days.

| Predictor | Odds ratio | 95% CI | p-value |
| --- | ---: | --- | ---: |
| Age, per 10 years | 1.1158 | 0.8201-1.5180 | 0.4855 |
| Male sex | 1.2994 | 0.3896-4.3341 | 0.6700 |
| Log length of stay | 1.6847 | 1.1189-2.5365 | 0.0125 |
| Prior encounters, 12 months | 1.0621 | 0.9457-1.1929 | 0.3092 |
| Chronic condition count | 0.8868 | 0.3387-2.3218 | 0.8067 |
| Outpatient follow-up within 30 days | 0.9978 | 0.2193-4.5402 | 0.9977 |

![Archived exploratory logistic regression forest plot](../../outputs/figures/logistic_regression_forest_plot_professional.png)

## Model Sensitivity Diagnostic

| Model | Follow-up variable | Converged | Pseudo R-squared | AIC | LLR p-value |
| --- | --- | --- | ---: | ---: | ---: |
| No follow-up covariate | None | Yes | 0.0665 | 107.88 | 0.2336 |
| With 7-day follow-up covariate | 7-day follow-up | No | Not estimable | Not estimable | Not estimable |
| With 14-day follow-up covariate | 14-day follow-up | Yes | 0.0806 | 108.43 | 0.2181 |
| With 30-day follow-up covariate | 30-day follow-up | Yes | 0.0665 | 109.88 | 0.3368 |

The 7-day follow-up model could not be estimated because no readmissions occurred among patients with observed 7-day outpatient follow-up, producing sparse-data or separation instability.

## Interpretation

This diagnostic supports the Version 1 framing: the current synthetic cohort is useful for validating cohort construction, temporal outcome engineering, and descriptive reporting, but it is not sufficient for predictive modeling. Any future predictive work should use a larger cohort, stricter discharge-time feature design, and separate model validation.
