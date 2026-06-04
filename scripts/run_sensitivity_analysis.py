from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import statsmodels.api as sm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.statistics_utils import format_p_value, wilson_ci  # noqa: E402

ANALYSIS_DIR = PROJECT_ROOT / "outputs" / "analysis"
TABLEAU_DIR = PROJECT_ROOT / "tableau_dashboard"

SQL_SCRIPTS = [
    "sql/01_profile_source_tables.sql",
    "sql/02_define_eligible_inpatient_encounters.sql",
    "sql/03_define_index_encounter.sql",
    "sql/04_define_postdischarge_utilization.sql",
    "sql/05_define_30_day_readmission.sql",
    "sql/06_create_final_analysis_dataset.sql",
]


def pct(numerator: int | float, denominator: int | float) -> float:
    return round(100 * numerator / denominator, 1) if denominator else 0.0


def load_final_analysis_dataset() -> pd.DataFrame:
    db_path = "/tmp/ehr_readmission_sensitivity_analysis.duckdb"
    con = duckdb.connect(db_path)
    try:
        for script in SQL_SCRIPTS:
            con.execute((PROJECT_ROOT / script).read_text())
        return con.execute("SELECT * FROM final_analysis_dataset").fetchdf()
    finally:
        con.close()


def add_rate_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["not_readmitted_count"] = df["patient_count"] - df["readmitted_30d_count"]
    df["readmission_rate_30d_percent"] = df.apply(
        lambda row: pct(row["readmitted_30d_count"], row["patient_count"]), axis=1
    )
    ci_low = []
    ci_high = []
    for row in df.itertuples(index=False):
        low, high = wilson_ci(int(row.readmitted_30d_count), int(row.patient_count))
        ci_low.append(round(low * 100, 1))
        ci_high.append(round(high * 100, 1))
    df["readmission_rate_ci_low_percent"] = ci_low
    df["readmission_rate_ci_high_percent"] = ci_high
    df["readmission_rate_ci_method"] = "Wilson score 95% CI"
    return df


def summarize_groups(df: pd.DataFrame, group_col: str, group_label: str) -> pd.DataFrame:
    rows = []
    for value, group in df.groupby(group_col, observed=True, sort=False):
        patient_count = len(group)
        readmitted_count = int(group["readmitted_30d"].sum())
        rows.append(
            {
                group_label: str(value),
                "patient_count": patient_count,
                "readmitted_30d_count": readmitted_count,
                "outpatient_followup_7d_count": int(group["outpatient_followup_7d"].sum()),
                "outpatient_followup_7d_percent": pct(
                    int(group["outpatient_followup_7d"].sum()), patient_count
                ),
                "outpatient_followup_14d_count": int(group["outpatient_followup_14d"].sum()),
                "outpatient_followup_14d_percent": pct(
                    int(group["outpatient_followup_14d"].sum()), patient_count
                ),
                "outpatient_followup_30d_count": int(group["outpatient_followup_30d"].sum()),
                "outpatient_followup_30d_percent": pct(
                    int(group["outpatient_followup_30d"].sum()), patient_count
                ),
                "ed_revisit_30d_count": int(group["ed_revisit_30d"].sum()),
                "ed_revisit_30d_percent": pct(int(group["ed_revisit_30d"].sum()), patient_count),
                "mean_prior_encounters_12mo": round(group["prior_encounters_12mo"].mean(), 2),
                "mean_prior_ed_visits_12mo": round(group["prior_ed_visits_12mo"].mean(), 2),
                "mean_length_of_stay_days": round(group["length_of_stay_days"].mean(), 2),
                "mean_chronic_condition_count": round(group["chronic_condition_count"].mean(), 2),
                "interpretation_note": (
                    "Descriptive synthetic-data subgroup summary; not causal or clinically validated."
                ),
            }
        )
    return add_rate_fields(pd.DataFrame(rows))


def build_prior_utilization_stratification(df: pd.DataFrame) -> pd.DataFrame:
    util_df = df.copy()
    util_df["prior_utilization_group"] = pd.cut(
        util_df["prior_encounters_12mo"],
        bins=[-1, 1, 4, np.inf],
        labels=[
            "Low prior utilization (0-1 encounters)",
            "Medium prior utilization (2-4 encounters)",
            "High prior utilization (5+ encounters)",
        ],
    )
    out = summarize_groups(util_df, "prior_utilization_group", "prior_utilization_group")
    out.insert(0, "sort_order", [1, 2, 3])
    return out


def build_prior_ed_use_stratification(df: pd.DataFrame) -> pd.DataFrame:
    ed_df = df.copy()
    ed_df["prior_ed_use_group"] = np.where(
        ed_df["prior_ed_visits_12mo"] > 0,
        "Any prior ED use",
        "No prior ED use",
    )
    out = summarize_groups(ed_df, "prior_ed_use_group", "prior_ed_use_group")
    order = {"No prior ED use": 1, "Any prior ED use": 2}
    out.insert(0, "sort_order", out["prior_ed_use_group"].map(order))
    return out.sort_values("sort_order")


def build_followup_window_sensitivity(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label, days, col in [
        ("0-7 days", 7, "outpatient_followup_7d"),
        ("0-14 days", 14, "outpatient_followup_14d"),
        ("0-30 days", 30, "outpatient_followup_30d"),
    ]:
        with_followup = df[df[col] == 1]
        without_followup = df[df[col] == 0]
        rows.append(
            {
                "followup_window": label,
                "followup_window_days": days,
                "cohort_patients": len(df),
                "followup_count": int(df[col].sum()),
                "followup_percent": pct(int(df[col].sum()), len(df)),
                "readmitted_with_followup_count": int(with_followup["readmitted_30d"].sum()),
                "readmission_rate_with_followup_percent": pct(
                    int(with_followup["readmitted_30d"].sum()), len(with_followup)
                ),
                "readmitted_without_followup_count": int(without_followup["readmitted_30d"].sum()),
                "readmission_rate_without_followup_percent": pct(
                    int(without_followup["readmitted_30d"].sum()), len(without_followup)
                ),
                "readmission_before_outpatient_followup_count": int(
                    df["readmission_before_outpatient_followup_flag"].sum()
                ),
                "interpretation_note": (
                    "Observed outpatient follow-up pattern only. Patients readmitted before follow-up "
                    "create timing bias, so this should not be interpreted as a causal effect."
                ),
            }
        )
    return pd.DataFrame(rows)


def prepare_model_df(df: pd.DataFrame) -> pd.DataFrame:
    model_df = df.copy()
    model_df["male_sex"] = (model_df["sex"] == "M").astype(int)
    model_df["age_per_10_years"] = model_df["age_at_index"] / 10
    model_df["log_length_of_stay"] = np.log1p(model_df["length_of_stay_days"])
    return model_df


def fit_logistic_model(
    df: pd.DataFrame,
    model_name: str,
    predictors: list[str],
    includes_followup: bool,
    followup_window_days: int | None,
) -> tuple[pd.DataFrame, dict[str, object]]:
    analysis_df = df[["readmitted_30d"] + predictors].dropna().copy()
    x = sm.add_constant(analysis_df[predictors].astype(float), has_constant="add")
    y = analysis_df["readmitted_30d"].astype(int)
    try:
        model = sm.Logit(y, x).fit(disp=0, maxiter=200)
        conf = model.conf_int()
        terms = pd.DataFrame(
            {
                "model_name": model_name,
                "includes_followup_variable": includes_followup,
                "followup_window_days": followup_window_days if followup_window_days else "",
                "term": model.params.index,
                "coefficient": model.params.values,
                "odds_ratio": np.exp(model.params.values),
                "ci_lower": np.exp(conf[0].values),
                "ci_upper": np.exp(conf[1].values),
                "p_value": model.pvalues.values,
            }
        )
        converged = bool(model.mle_retvals.get("converged", False))
        model_note = {
            "model_name": model_name,
            "includes_followup_variable": includes_followup,
            "followup_window_days": followup_window_days if followup_window_days else "",
            "n_observations": int(model.nobs),
            "readmission_events": int(y.sum()),
            "converged": converged,
            "pseudo_r_squared": round(float(model.prsquared), 4),
            "aic": round(float(model.aic), 2),
            "bic": round(float(model.bic), 2),
            "llr_p_value": round(float(model.llr_pvalue), 4),
            "interpretation_note": (
                "Exploratory adjusted association model using synthetic data. Compare model sets "
                "for sensitivity to follow-up timing variables; do not interpret causally."
            )
            if converged
            else (
                "Model did not converge cleanly in this synthetic cohort; treat coefficients "
                "as unstable and do not interpret as effect estimates."
            ),
        }
    except Exception as exc:
        terms = pd.DataFrame(
            {
                "model_name": model_name,
                "includes_followup_variable": includes_followup,
                "followup_window_days": followup_window_days if followup_window_days else "",
                "term": ["const"] + predictors,
                "coefficient": np.nan,
                "odds_ratio": np.nan,
                "ci_lower": np.nan,
                "ci_upper": np.nan,
                "p_value": np.nan,
            }
        )
        model_note = {
            "model_name": model_name,
            "includes_followup_variable": includes_followup,
            "followup_window_days": followup_window_days if followup_window_days else "",
            "n_observations": int(len(analysis_df)),
            "readmission_events": int(y.sum()),
            "converged": False,
            "pseudo_r_squared": np.nan,
            "aic": np.nan,
            "bic": np.nan,
            "llr_p_value": np.nan,
            "interpretation_note": (
                f"Model could not be estimated ({type(exc).__name__}: {exc}). "
                "This is documented as sparse-data or separation instability, not as a clinical finding."
            ),
        }
    return terms, model_note


def build_model_sensitivity_outputs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    model_df = prepare_model_df(df)
    base_predictors = [
        "age_per_10_years",
        "male_sex",
        "log_length_of_stay",
        "prior_encounters_12mo",
        "chronic_condition_count",
    ]
    model_specs = [
        ("No follow-up covariate", base_predictors, False, None),
        ("With 7-day follow-up covariate", base_predictors + ["outpatient_followup_7d"], True, 7),
        ("With 14-day follow-up covariate", base_predictors + ["outpatient_followup_14d"], True, 14),
        ("With 30-day follow-up covariate", base_predictors + ["outpatient_followup_30d"], True, 30),
    ]
    term_frames = []
    notes = []
    for model_name, predictors, includes_followup, window_days in model_specs:
        terms, note = fit_logistic_model(model_df, model_name, predictors, includes_followup, window_days)
        term_frames.append(terms)
        notes.append(note)

    model_terms = pd.concat(term_frames, ignore_index=True)
    term_labels = {
        "const": "Intercept",
        "age_per_10_years": "Age, per 10 years",
        "male_sex": "Male sex",
        "log_length_of_stay": "Log length of stay",
        "prior_encounters_12mo": "Prior encounters, 12 months",
        "chronic_condition_count": "Chronic condition count",
        "outpatient_followup_7d": "Outpatient follow-up within 7 days",
        "outpatient_followup_14d": "Outpatient follow-up within 14 days",
        "outpatient_followup_30d": "Outpatient follow-up within 30 days",
    }
    model_terms["label"] = model_terms["term"].map(term_labels).fillna(model_terms["term"])
    model_convergence = {note["model_name"]: note["converged"] for note in notes}
    model_terms["model_converged"] = model_terms["model_name"].map(model_convergence)
    model_terms["term_interpretation_note"] = np.where(
        model_terms["model_converged"],
        "Exploratory adjusted association estimate; synthetic data only.",
        "Model did not converge cleanly; coefficient and interval should not be interpreted.",
    )
    model_terms = model_terms.replace([np.inf, -np.inf], np.nan)
    for col in ["coefficient", "odds_ratio", "ci_lower", "ci_upper", "p_value"]:
        model_terms[col] = model_terms[col].round(4)

    model_comparison = pd.DataFrame(notes)
    model_comparison["formatted_llr_p_value"] = model_comparison["llr_p_value"].apply(
        lambda value: format_p_value(value) if pd.notna(value) else "Not estimable"
    )
    model_comparison["comparison_note"] = (
        "Models are compared descriptively to assess sensitivity to observed follow-up timing variables. "
        "Lower AIC/BIC is not a claim of clinical validity."
    )

    without_followup = model_terms.loc[model_terms["model_name"] == "No follow-up covariate"].copy()
    with_followup = model_terms.loc[model_terms["includes_followup_variable"] == True].copy()  # noqa: E712
    return model_comparison, without_followup, with_followup


def validate_outputs(outputs: dict[str, pd.DataFrame]) -> list[str]:
    checks = {
        "Prior utilization groups have patient counts": outputs["prior_utilization_stratification"][
            "patient_count"
        ].sum()
        > 0,
        "Prior ED use groups have patient counts": outputs["prior_ed_use_stratification"][
            "patient_count"
        ].sum()
        > 0,
        "Follow-up windows are monotonic": outputs["followup_window_sensitivity"][
            "followup_count"
        ].is_monotonic_increasing,
        "Model comparison p-values are in range": outputs["model_comparison_sensitivity"][
            "llr_p_value"
        ].dropna().between(0, 1).all(),
    }
    if not all(checks.values()):
        failed = [label for label, passed in checks.items() if not passed]
        raise ValueError(f"Sensitivity validation failed: {failed}")
    return [f"{'PASS' if passed else 'FAIL'}: {label}" for label, passed in checks.items()]


def run_sensitivity_analysis() -> dict[str, pd.DataFrame]:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    TABLEAU_DIR.mkdir(parents=True, exist_ok=True)
    df = load_final_analysis_dataset()

    model_comparison, model_without_followup, model_with_followup = build_model_sensitivity_outputs(df)
    outputs = {
        "prior_utilization_stratification": build_prior_utilization_stratification(df),
        "prior_ed_use_stratification": build_prior_ed_use_stratification(df),
        "followup_window_sensitivity": build_followup_window_sensitivity(df),
        "model_comparison_sensitivity": model_comparison,
        "model_without_followup_results": model_without_followup,
        "model_with_followup_results": model_with_followup,
    }
    validation_messages = validate_outputs(outputs)

    for name, out_df in outputs.items():
        out_df.to_csv(ANALYSIS_DIR / f"{name}.csv", index=False)
        out_df.to_csv(TABLEAU_DIR / f"{name}.csv", index=False)

    print("Created sensitivity analysis outputs:")
    for name, out_df in outputs.items():
        print(f"- outputs/analysis/{name}.csv ({out_df.shape[0]} rows x {out_df.shape[1]} columns)")
        print(f"- tableau_dashboard/{name}.csv ({out_df.shape[0]} rows x {out_df.shape[1]} columns)")
    print("\nValidation checks:")
    for message in validation_messages:
        print(f"- {message}")

    return outputs


if __name__ == "__main__":
    run_sensitivity_analysis()
