from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.statistics_utils import (  # noqa: E402
    choose_subgroup_test,
    format_p_value,
    subgroup_size_note,
    wilson_ci,
)


TABLEAU_DIR = PROJECT_ROOT / "tableau_dashboard"
BI_DIR = PROJECT_ROOT / "outputs" / "bi"
ANALYSIS_DIR = PROJECT_ROOT / "outputs" / "analysis"
VALIDATION_DIR = PROJECT_ROOT / "outputs" / "validation"


def parse_count_percent(value: object) -> tuple[int | None, float | None]:
    match = re.match(r"\s*(\d+)\s*\(([-0-9.]+)%\)", str(value))
    if not match:
        return None, None
    return int(match.group(1)), float(match.group(2))


def percent(numerator: int | float, denominator: int | float) -> float:
    return round(100 * numerator / denominator, 1) if denominator else 0.0


def add_wilson_fields(
    df: pd.DataFrame,
    count_col: str = "readmitted_30d_count",
    denominator_col: str = "patient_count",
) -> pd.DataFrame:
    df = df.copy()
    low_values: list[float] = []
    high_values: list[float] = []
    for row in df.itertuples(index=False):
        count = int(getattr(row, count_col))
        denominator = int(getattr(row, denominator_col))
        low, high = wilson_ci(count, denominator)
        low_values.append(round(low * 100, 1))
        high_values.append(round(high * 100, 1))
    df["readmission_rate_ci_low_percent"] = low_values
    df["readmission_rate_ci_high_percent"] = high_values
    df["readmission_rate_ci_method"] = "Wilson score 95% CI"
    df["readmission_rate_note"] = (
        "Descriptive subgroup readmission rate with Wilson 95% confidence interval; "
        "synthetic data only."
    )
    return df


def load_inputs() -> dict[str, pd.DataFrame | pd.Series]:
    table1 = pd.read_csv(ANALYSIS_DIR / "table1_baseline_characteristics.csv")
    table1["variable_filled"] = table1["variable"].replace("", pd.NA).ffill()
    return {
        "cohort": pd.read_csv(BI_DIR / "cohort_summary_table.csv").iloc[0],
        "readmission": pd.read_csv(BI_DIR / "readmission_kpi_table.csv").iloc[0],
        "followup": pd.read_csv(BI_DIR / "followup_timing_table.csv"),
        "ed": pd.read_csv(BI_DIR / "ed_revisit_table.csv").iloc[0],
        "demo": pd.read_csv(BI_DIR / "demographic_utilization_summary_table.csv"),
        "table1": table1,
        "attrition": pd.read_csv(VALIDATION_DIR / "cohort_attrition_counts.csv"),
        "index_check": pd.read_csv(VALIDATION_DIR / "index_encounter_check.csv").iloc[0],
        "date_checks": pd.read_csv(VALIDATION_DIR / "date_validity_checks.csv"),
        "missingness": pd.read_csv(VALIDATION_DIR / "missingness_report.csv"),
        "readmit_timing": pd.read_csv(VALIDATION_DIR / "readmission_timing_validation.csv").iloc[0],
        "followup_timing": pd.read_csv(VALIDATION_DIR / "outpatient_followup_timing_validation.csv").iloc[0],
    }


def build_kpi_summary(inputs: dict[str, pd.DataFrame | pd.Series]) -> pd.DataFrame:
    cohort = inputs["cohort"]
    readmission = inputs["readmission"]
    followup = inputs["followup"]
    ed = inputs["ed"]
    cohort_n = int(cohort["cohort_patients"])
    followup_30 = followup.loc[followup["followup_window_days"] == 30].iloc[0]

    return pd.DataFrame(
        [
            {
                "kpi_name": "Final analytic cohort",
                "kpi_category": "Cohort",
                "count": cohort_n,
                "denominator": cohort_n,
                "percent": 100.0,
                "display_value": f"{cohort_n:,} patients",
                "interpretation_note": "Adult patients with one first eligible index inpatient encounter. Synthetic data only.",
            },
            {
                "kpi_name": "30-day inpatient readmission",
                "kpi_category": "Outcome",
                "count": int(readmission["readmitted_30d_count"]),
                "denominator": int(readmission["cohort_patients"]),
                "percent": float(readmission["readmission_rate_30d_percent"]),
                "display_value": f"{float(readmission['readmission_rate_30d_percent']):.1f}%",
                "interpretation_note": "All-cause inpatient readmission within 30 days of index discharge. Descriptive only.",
            },
            {
                "kpi_name": "30-day outpatient follow-up",
                "kpi_category": "Utilization",
                "count": int(followup_30["followup_count"]),
                "denominator": cohort_n,
                "percent": float(followup_30["followup_percent"]),
                "display_value": f"{float(followup_30['followup_percent']):.1f}%",
                "interpretation_note": "Outpatient or ambulatory follow-up within 30 days. Not interpreted causally.",
            },
            {
                "kpi_name": "30-day ED revisit",
                "kpi_category": "Utilization",
                "count": int(ed["ed_revisit_30d_count"]),
                "denominator": int(ed["cohort_patients"]),
                "percent": float(ed["ed_revisit_30d_percent"]),
                "display_value": f"{float(ed['ed_revisit_30d_percent']):.1f}%",
                "interpretation_note": "ED revisit within 30 days. Rare event in this synthetic cohort.",
            },
            {
                "kpi_name": "Any post-discharge encounter within 30 days",
                "kpi_category": "Utilization",
                "count": int(ed["any_postdischarge_encounter_30d_count"]),
                "denominator": int(ed["cohort_patients"]),
                "percent": float(ed["any_postdischarge_encounter_30d_percent"]),
                "display_value": f"{float(ed['any_postdischarge_encounter_30d_percent']):.1f}%",
                "interpretation_note": "Any observed post-discharge encounter within 30 days.",
            },
        ]
    )


def build_readmission_by_age_group(inputs: dict[str, pd.DataFrame | pd.Series]) -> pd.DataFrame:
    demo = inputs["demo"]
    age = demo.loc[demo["summary_domain"] == "age_group"].copy()
    age_order = {"Under 65": 1, "65+": 2}
    age["sort_order"] = age["category"].map(age_order).fillna(99).astype(int)
    age = age.sort_values("sort_order")
    age = age[
        [
            "category",
            "patient_count",
            "patient_percent_within_domain",
            "readmitted_30d_count",
            "readmission_rate_30d_percent",
            "outpatient_followup_30d_count",
            "outpatient_followup_30d_percent",
            "ed_revisit_30d_count",
            "ed_revisit_30d_percent",
            "mean_length_of_stay_days",
            "mean_prior_encounters_12mo",
            "mean_chronic_condition_count",
            "sort_order",
        ]
    ].rename(columns={"category": "age_group"})
    age["not_readmitted_count"] = age["patient_count"] - age["readmitted_30d_count"]
    age = add_wilson_fields(age)

    contingency = age[["readmitted_30d_count", "not_readmitted_count"]].to_numpy()
    test = choose_subgroup_test(contingency)
    age["comparison_test"] = test["test_name"]
    age["comparison_p_value"] = round(test["p_value"], 4)
    age["comparison_interpretation"] = (
        f"Exploratory age-group comparison using {test['test_name']} "
        f"(p={format_p_value(test['p_value'])}). {test['reason']} "
        "Synthetic subgroup comparison only; not causal or clinically validated."
    )
    age["interpretation_note"] = (
        "Synthetic subgroup summary; descriptive only. Small readmission counts should not be overinterpreted."
    )
    return age


def build_readmission_by_condition_group(inputs: dict[str, pd.DataFrame | pd.Series]) -> pd.DataFrame:
    table1 = inputs["table1"]
    condition_labels = {
        "Diabetes flag": "Diabetes",
        "Hypertension flag": "Hypertension",
        "CKD flag": "Chronic kidney disease",
        "COPD flag": "COPD",
    }

    rows = []
    for variable, label in condition_labels.items():
        p_value_row = table1.loc[table1["variable"] == variable, "p_value"]
        p_value = p_value_row.iloc[0] if not p_value_row.empty else ""
        row = table1.loc[
            (table1["variable_filled"] == variable) & (table1["level"].astype(str) == "1")
        ].iloc[0]
        patient_count, patient_percent = parse_count_percent(row["overall"])
        not_readmitted_count, _ = parse_count_percent(row["not_readmitted"])
        readmitted_count, _ = parse_count_percent(row["readmitted"])
        rows.append(
            {
                "condition_group": label,
                "patient_count": patient_count,
                "patient_percent": patient_percent,
                "readmitted_30d_count": readmitted_count,
                "not_readmitted_count": not_readmitted_count,
                "readmission_rate_30d_percent": percent(readmitted_count, patient_count),
                "p_value": p_value,
                "interpretation_note": "Derived from simplified Synthea condition flags in aggregate Table 1; descriptive only.",
            }
        )

    condition = pd.DataFrame(rows).sort_values("condition_group")
    condition = add_wilson_fields(condition)
    condition["subgroup_sample_size_note"] = condition["patient_count"].apply(subgroup_size_note)
    return condition


def build_utilization_summary(inputs: dict[str, pd.DataFrame | pd.Series]) -> pd.DataFrame:
    cohort = inputs["cohort"]
    readmission = inputs["readmission"]
    followup = inputs["followup"]
    ed = inputs["ed"]
    cohort_n = int(cohort["cohort_patients"])

    rows = []
    for _, row in followup.iterrows():
        rows.append(
            {
                "measure_name": f"Outpatient follow-up {row['followup_window']}",
                "measure_group": "Outpatient follow-up",
                "window_days": int(row["followup_window_days"]),
                "count": int(row["followup_count"]),
                "denominator": cohort_n,
                "percent": float(row["followup_percent"]),
                "mean_days_to_event": float(row["mean_days_to_first_followup"]),
                "interpretation_note": "Cumulative outpatient or ambulatory follow-up window after discharge.",
            }
        )
    rows.extend(
        [
            {
                "measure_name": "30-day ED revisit",
                "measure_group": "ED revisit",
                "window_days": 30,
                "count": int(ed["ed_revisit_30d_count"]),
                "denominator": int(ed["cohort_patients"]),
                "percent": float(ed["ed_revisit_30d_percent"]),
                "mean_days_to_event": "",
                "interpretation_note": "ED revisit within 30 days; secondary utilization measure.",
            },
            {
                "measure_name": "30-day inpatient readmission",
                "measure_group": "Readmission",
                "window_days": 30,
                "count": int(readmission["readmitted_30d_count"]),
                "denominator": int(readmission["cohort_patients"]),
                "percent": float(readmission["readmission_rate_30d_percent"]),
                "mean_days_to_event": float(readmission["mean_days_to_readmission"]),
                "interpretation_note": "Primary outcome; all-cause inpatient readmission within 30 days.",
            },
            {
                "measure_name": "Any post-discharge encounter within 30 days",
                "measure_group": "Any encounter",
                "window_days": 30,
                "count": int(ed["any_postdischarge_encounter_30d_count"]),
                "denominator": int(ed["cohort_patients"]),
                "percent": float(ed["any_postdischarge_encounter_30d_percent"]),
                "mean_days_to_event": "",
                "interpretation_note": "Any observed post-discharge encounter within 30 days.",
            },
        ]
    )
    return pd.DataFrame(rows)


def build_data_quality_summary(inputs: dict[str, pd.DataFrame | pd.Series]) -> pd.DataFrame:
    cohort = inputs["cohort"]
    attrition = inputs["attrition"]
    index_check = inputs["index_check"]
    date_checks = inputs["date_checks"]
    missingness = inputs["missingness"]
    readmit_timing = inputs["readmit_timing"]
    followup_timing = inputs["followup_timing"]

    cohort_n = int(cohort["cohort_patients"])
    attr_lookup = dict(zip(attrition["step"], attrition["record_count"]))
    final_date = date_checks.loc[date_checks["dataset"] == "final_analysis_dataset"].iloc[0]
    invalid_final_dates = int(
        final_date["missing_start"]
        + final_date["missing_stop"]
        + final_date["invalid_start"]
        + final_date["invalid_stop"]
        + final_date["stop_before_start"]
    )

    rows = [
        {
            "quality_domain": "Cohort construction",
            "check_name": "Final analysis dataset rows",
            "value": int(attr_lookup.get("final_analysis_dataset_rows", cohort_n)),
            "denominator": cohort_n,
            "percent": 100.0,
            "status": "Pass",
            "interpretation_note": "Final aggregate cohort available for dashboard reporting.",
        },
        {
            "quality_domain": "Index encounter",
            "check_name": "One index encounter per patient",
            "value": int(index_check["index_rows"] == index_check["distinct_patients"]),
            "denominator": 1,
            "percent": 100.0
            if index_check["index_rows"] == index_check["distinct_patients"]
            else 0.0,
            "status": "Pass"
            if index_check["index_rows"] == index_check["distinct_patients"]
            else "Review",
            "interpretation_note": f"{int(index_check['index_rows'])} index rows and {int(index_check['distinct_patients'])} distinct patients.",
        },
        {
            "quality_domain": "Index encounter",
            "check_name": "Duplicate patient index rows",
            "value": int(index_check["duplicate_patient_index_rows"]),
            "denominator": int(index_check["index_rows"]),
            "percent": percent(
                int(index_check["duplicate_patient_index_rows"]), int(index_check["index_rows"])
            ),
            "status": "Pass" if int(index_check["duplicate_patient_index_rows"]) == 0 else "Review",
            "interpretation_note": "Duplicate patient index rows should be zero.",
        },
        {
            "quality_domain": "Date validity",
            "check_name": "Invalid or missing final encounter dates",
            "value": invalid_final_dates,
            "denominator": int(final_date["row_count"]),
            "percent": percent(invalid_final_dates, int(final_date["row_count"])),
            "status": "Pass" if invalid_final_dates == 0 else "Review",
            "interpretation_note": "Missing, invalid, or temporally inconsistent final analysis dates.",
        },
        {
            "quality_domain": "Outcome derivation",
            "check_name": "Missing readmission outcome rows",
            "value": int(readmit_timing["missing_readmission_outcome_rows"]),
            "denominator": int(readmit_timing["final_rows"]),
            "percent": percent(
                int(readmit_timing["missing_readmission_outcome_rows"]),
                int(readmit_timing["final_rows"]),
            ),
            "status": "Pass" if int(readmit_timing["missing_readmission_outcome_rows"]) == 0 else "Review",
            "interpretation_note": "Primary outcome should be populated for all final analysis rows.",
        },
        {
            "quality_domain": "Follow-up timing",
            "check_name": "Non-monotonic follow-up window rows",
            "value": int(followup_timing["non_monotonic_followup_window_rows"]),
            "denominator": int(followup_timing["final_rows"]),
            "percent": percent(
                int(followup_timing["non_monotonic_followup_window_rows"]),
                int(followup_timing["final_rows"]),
            ),
            "status": "Pass"
            if int(followup_timing["non_monotonic_followup_window_rows"]) == 0
            else "Review",
            "interpretation_note": "7/14/30-day outpatient follow-up flags should be monotonic.",
        },
    ]

    expected_missing = {
        "days_to_readmission",
        "readmission_encounter_id",
        "days_to_first_outpatient_followup",
        "days_to_first_postdischarge_encounter",
    }
    for _, row in missingness.head(8).iterrows():
        rows.append(
            {
                "quality_domain": "Missingness",
                "check_name": f"Missingness: {row['variable']}",
                "value": int(row["missing_count"]),
                "denominator": int(row["row_count"]),
                "percent": float(row["missing_percent"]),
                "status": "Expected" if row["variable"] in expected_missing else "Review",
                "interpretation_note": "Timing fields are missing when the corresponding event is not observed; other variables require review.",
            }
        )
    return pd.DataFrame(rows)


def validate_tableau_outputs(age: pd.DataFrame, condition: pd.DataFrame) -> list[str]:
    checks = []
    combined = pd.concat(
        [
            age.assign(source_table="readmission_by_age_group"),
            condition.assign(source_table="readmission_by_condition_group"),
        ],
        ignore_index=True,
        sort=False,
    )

    ci_low_ok = bool((combined["readmission_rate_ci_low_percent"] >= 0).all())
    ci_high_ok = bool((combined["readmission_rate_ci_high_percent"] <= 100).all())
    count_ok = bool(
        (
            combined["patient_count"]
            == combined["readmitted_30d_count"] + combined["not_readmitted_count"]
        ).all()
    )
    p_values = age["comparison_p_value"].dropna()
    p_values_ok = bool(((p_values >= 0) & (p_values <= 1)).all())

    validations = {
        "CI lower bound is never below 0": ci_low_ok,
        "CI upper bound is never above 100": ci_high_ok,
        "patient_count equals readmitted_30d_count + not_readmitted_count": count_ok,
        "age-group comparison p-values are within 0-1": p_values_ok,
    }
    for label, passed in validations.items():
        checks.append(f"{'PASS' if passed else 'FAIL'}: {label}")
    if not all(validations.values()):
        raise ValueError("One or more Tableau statistical export validation checks failed.")
    return checks


def build_tableau_exports(include_sensitivity: bool = True) -> dict[str, pd.DataFrame]:
    TABLEAU_DIR.mkdir(exist_ok=True)
    inputs = load_inputs()

    outputs = {
        "kpi_summary": build_kpi_summary(inputs),
        "readmission_by_age_group": build_readmission_by_age_group(inputs),
        "readmission_by_condition_group": build_readmission_by_condition_group(inputs),
        "utilization_summary": build_utilization_summary(inputs),
        "data_quality_summary": build_data_quality_summary(inputs),
    }

    validation_messages = validate_tableau_outputs(
        outputs["readmission_by_age_group"], outputs["readmission_by_condition_group"]
    )

    for name, df in outputs.items():
        df.to_csv(TABLEAU_DIR / f"{name}.csv", index=False)

    print("Created Tableau dashboard exports:")
    for name, df in outputs.items():
        print(f"- tableau_dashboard/{name}.csv ({df.shape[0]} rows x {df.shape[1]} columns)")
    print("\nValidation checks:")
    for message in validation_messages:
        print(f"- {message}")

    if include_sensitivity:
        from scripts.run_sensitivity_analysis import run_sensitivity_analysis

        sensitivity_outputs = run_sensitivity_analysis()
        outputs.update(sensitivity_outputs)

    return outputs


if __name__ == "__main__":
    build_tableau_exports()
