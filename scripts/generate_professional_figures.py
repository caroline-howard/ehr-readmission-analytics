from pathlib import Path
import os
import tempfile
import textwrap

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "ehr_readmission_matplotlib")
)

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
BI_DIR = OUTPUTS_DIR / "bi"
ANALYSIS_DIR = OUTPUTS_DIR / "analysis"
VALIDATION_DIR = OUTPUTS_DIR / "validation"
FIGURE_DIR = OUTPUTS_DIR / "figures"

COLORS = {
    "navy": "#1f3347",
    "blue": "#2f6f9f",
    "teal": "#2f8f83",
    "green": "#6aa84f",
    "amber": "#c58b2b",
    "red": "#b85c5c",
    "gray": "#667085",
    "light_gray": "#f3f6f8",
    "grid": "#dfe7ee",
    "border": "#d5dde5",
    "white": "#ffffff",
}


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing expected aggregate output: {path}. "
            "Run the SQL/notebook workflow before regenerating figures."
        )
    return pd.read_csv(path)


def pct(value: float) -> str:
    return f"{value:.1f}%"


def style_panel(ax, title: str | None = None):
    ax.set_facecolor(COLORS["white"])
    for spine in ax.spines.values():
        spine.set_color(COLORS["border"])
        spine.set_linewidth(1)
    ax.tick_params(colors=COLORS["gray"], labelsize=9)
    if title:
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=COLORS["navy"], pad=10)


def save(fig, filename: str):
    path = FIGURE_DIR / filename
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Created {path.relative_to(PROJECT_ROOT)}")


def add_kpi_card(ax, label: str, value: str, detail: str):
    ax.set_axis_off()
    box = FancyBboxPatch(
        (0, 0),
        1,
        1,
        boxstyle="round,pad=0.02,rounding_size=0.018",
        linewidth=1,
        edgecolor=COLORS["border"],
        facecolor=COLORS["white"],
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(box)
    ax.text(0.06, 0.72, label.upper(), transform=ax.transAxes, fontsize=8.5, color=COLORS["gray"], fontweight="bold")
    ax.text(0.06, 0.34, value, transform=ax.transAxes, fontsize=24, color=COLORS["navy"], fontweight="bold")
    ax.text(0.06, 0.13, detail, transform=ax.transAxes, fontsize=9.5, color=COLORS["gray"])


def plot_followup_curve(ax, followup: pd.DataFrame, title: str = "Cumulative outpatient follow-up"):
    days = [0] + followup["followup_window_days"].astype(int).tolist()
    percents = [0.0] + followup["followup_percent"].astype(float).tolist()
    ax.plot(days, percents, marker="o", color=COLORS["teal"], linewidth=2.5, markersize=6)
    ax.fill_between(days, percents, color=COLORS["teal"], alpha=0.12)
    ax.set_xlim(0, 30)
    ax.set_ylim(0, max(30, max(percents) + 5))
    ax.set_xlabel("Days after discharge", color=COLORS["gray"])
    ax.set_ylabel("Percent with outpatient follow-up", color=COLORS["gray"])
    ax.set_xticks([0, 7, 14, 30])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
    style_panel(ax, title)
    for x, y in zip(days[1:], percents[1:]):
        ax.text(x, y + 1.1, pct(y), ha="center", fontsize=9.5, color=COLORS["navy"], fontweight="bold")


def plot_prior_utilization(ax, prior: pd.DataFrame, title: str = "Readmission by prior utilization"):
    labels = ["Low\n0-1", "Medium\n2-4", "High\n5+"]
    values = prior["readmission_rate_30d_percent"].astype(float).tolist()
    counts = prior["readmitted_30d_count"].astype(int).tolist()
    totals = prior["patient_count"].astype(int).tolist()
    bars = ax.bar(labels, values, color=[COLORS["blue"], COLORS["teal"], COLORS["red"]], width=0.62)
    ax.set_ylabel("30-day readmission rate", color=COLORS["gray"])
    ax.set_ylim(0, max(values) + 5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    style_panel(ax, title)
    for bar, value, count, total in zip(bars, values, counts, totals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.6,
            f"{value:.1f}%\n{count}/{total}",
            ha="center",
            fontsize=9,
            color=COLORS["navy"],
            fontweight="bold",
        )


def plot_age_group(ax, risk: pd.DataFrame):
    age = risk[risk["stratification_domain"] == "age_group"].copy()
    age["category"] = pd.Categorical(age["category"], ["Under 65", "65+"], ordered=True)
    age = age.sort_values("category")
    ax.bar(age["category"], age["patient_count"], color=[COLORS["blue"], COLORS["teal"]], width=0.6)
    ax.set_ylabel("Patients", color=COLORS["gray"])
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    style_panel(ax, "Age group summary")
    for i, row in enumerate(age.itertuples()):
        ax.text(i, row.patient_count + 4, f"{int(row.patient_count)}", ha="center", fontsize=9.5, color=COLORS["navy"], fontweight="bold")


def plot_chronic_burden(ax, risk: pd.DataFrame):
    chronic = risk[risk["stratification_domain"] == "chronic_condition_count"].copy()
    chronic["category"] = chronic["category"].astype(str)
    ax.bar(chronic["category"], chronic["patient_count"], color=COLORS["blue"], width=0.65)
    ax.set_xlabel("Chronic condition count", color=COLORS["gray"])
    ax.set_ylabel("Patients", color=COLORS["gray"])
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    style_panel(ax, "Chronic condition burden")
    for i, row in enumerate(chronic.itertuples()):
        ax.text(i, row.patient_count + 4, f"{int(row.patient_count)}", ha="center", fontsize=9, color=COLORS["navy"], fontweight="bold")


def prepare_regression() -> pd.DataFrame:
    reg = read_csv(ANALYSIS_DIR / "logistic_regression_results.csv")
    reg = reg[reg["term"] != "const"].copy()
    reg = reg.sort_values("odds_ratio")
    return reg


def plot_forest(ax, reg: pd.DataFrame, title: str, compact: bool = False):
    labels = reg["label"].tolist()
    y = np.arange(len(reg))
    color = np.where(reg["p_value"].astype(float) < 0.05, COLORS["red"], COLORS["blue"])
    ax.errorbar(
        reg["odds_ratio"],
        y,
        xerr=[reg["odds_ratio"] - reg["ci_lower"], reg["ci_upper"] - reg["odds_ratio"]],
        fmt="o",
        color=COLORS["navy"],
        ecolor=COLORS["gray"],
        elinewidth=1.2,
        capsize=3,
        markersize=0,
    )
    ax.scatter(reg["odds_ratio"], y, s=54 if not compact else 36, c=color, zorder=3)
    ax.axvline(1, color=COLORS["gray"], linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9 if not compact else 7.5)
    ax.set_xlabel("Odds ratio, log scale", color=COLORS["gray"], fontsize=9)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8)
    style_panel(ax, title)
    if not compact:
        x_text = reg["ci_upper"].max() * 1.35
        ax.set_xlim(max(0.15, reg["ci_lower"].min() * 0.65), x_text * 1.7)
        for yi, row in enumerate(reg.itertuples()):
            label = f"OR {row.odds_ratio:.2f} ({row.ci_lower:.2f}-{row.ci_upper:.2f})"
            if row.p_value < 0.05:
                label += " *"
            ax.text(x_text, yi, label, va="center", fontsize=8.8, color=COLORS["navy"])
    else:
        ax.set_xlim(max(0.2, reg["ci_lower"].min() * 0.75), reg["ci_upper"].max() * 1.25)
    ax.invert_yaxis()


def make_dashboard():
    cohort = read_csv(BI_DIR / "cohort_summary_table.csv").iloc[0]
    readmission = read_csv(BI_DIR / "readmission_kpi_table.csv").iloc[0]
    followup = read_csv(BI_DIR / "followup_timing_table.csv")
    ed = read_csv(BI_DIR / "ed_revisit_table.csv").iloc[0]
    prior = read_csv(ANALYSIS_DIR / "prior_utilization_group_summary.csv")
    risk = read_csv(ANALYSIS_DIR / "risk_stratification_summary.csv")
    reg = prepare_regression()

    fig = plt.figure(figsize=(16, 13), facecolor=COLORS["light_gray"])
    gs = fig.add_gridspec(5, 12, left=0.04, right=0.98, top=0.90, bottom=0.055, hspace=0.75, wspace=0.60)
    fig.text(0.04, 0.965, "Post-Discharge Utilization Dashboard", fontsize=25, fontweight="bold", color=COLORS["navy"])
    fig.text(
        0.04,
        0.935,
        "Synthetic Synthea EHR cohort | Aggregate portfolio dashboard mockup | Not for clinical decision-making",
        fontsize=10.5,
        color=COLORS["gray"],
    )

    kpis = [
        ("Final analytic cohort", f"{int(cohort['cohort_patients']):,}", "patients"),
        ("30-day readmission", pct(readmission["readmission_rate_30d_percent"]), f"{int(readmission['readmitted_30d_count'])} patients"),
        (
            "30-day outpatient follow-up",
            pct(followup.loc[followup["followup_window_days"] == 30, "followup_percent"].iloc[0]),
            f"{int(followup.loc[followup['followup_window_days'] == 30, 'followup_count'].iloc[0])} patients",
        ),
        ("30-day ED revisit", pct(ed["ed_revisit_30d_percent"]), f"{int(ed['ed_revisit_30d_count'])} patients"),
    ]
    for idx, (label, value, detail) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, idx * 3 : (idx + 1) * 3])
        add_kpi_card(ax, label, value, detail)

    plot_followup_curve(fig.add_subplot(gs[1, 0:6]), followup)
    ax_prior = fig.add_subplot(gs[1, 6:12])
    plot_prior_utilization(ax_prior, prior)
    ax_prior.set_ylabel("")
    plot_age_group(fig.add_subplot(gs[2, 0:6]), risk)
    plot_chronic_burden(fig.add_subplot(gs[2, 6:12]), risk)
    plot_forest(fig.add_subplot(gs[3:5, 0:12]), reg, "Model insight: exploratory logistic regression odds ratios", compact=False)

    fig.text(
        0.04,
        0.02,
        "Synthetic-data demonstration only. Dashboard values are aggregate portfolio outputs and are not clinical evidence.",
        fontsize=9,
        color=COLORS["gray"],
    )
    save(fig, "dashboard_mockup_professional.png")


def make_cohort_flow():
    attrition = read_csv(VALIDATION_DIR / "cohort_attrition_counts.csv")
    lookup = dict(zip(attrition["step"], attrition["record_count"]))
    steps = [
        ("Source encounters", lookup["source_encounters"]),
        ("Source inpatient encounters", lookup["source_inpatient_encounters"]),
        ("Eligible adult inpatient encounters", lookup["eligible_adult_inpatient_encounters"]),
        ("Patients with eligible adult inpatient encounter", lookup["patients_with_eligible_adult_inpatient_encounter"]),
        ("Final analysis dataset", lookup["final_analysis_dataset_rows"]),
    ]
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=COLORS["white"])
    ax.set_axis_off()
    ax.set_title("Figure 1. Cohort attrition flow diagram", loc="left", fontsize=17, fontweight="bold", color=COLORS["navy"], pad=16)
    y_positions = np.linspace(0.82, 0.14, len(steps))
    for idx, ((label, count), y) in enumerate(zip(steps, y_positions)):
        box = FancyBboxPatch(
            (0.18, y - 0.055),
            0.64,
            0.11,
            boxstyle="round,pad=0.018,rounding_size=0.018",
            linewidth=1.2,
            edgecolor=COLORS["border"],
            facecolor=COLORS["light_gray"] if idx < len(steps) - 1 else "#e8f3f1",
            transform=ax.transAxes,
        )
        ax.add_patch(box)
        ax.text(0.22, y + 0.012, label, transform=ax.transAxes, fontsize=12, color=COLORS["navy"], fontweight="bold", va="center")
        ax.text(0.78, y + 0.012, f"{int(count):,}", transform=ax.transAxes, fontsize=12, color=COLORS["navy"], fontweight="bold", va="center", ha="right")
        if idx < len(steps) - 1:
            ax.annotate("", xy=(0.5, y_positions[idx + 1] + 0.07), xytext=(0.5, y - 0.07), xycoords=ax.transAxes, arrowprops={"arrowstyle": "->", "color": COLORS["gray"], "lw": 1.3})
    ax.text(0.18, 0.035, "Counts are derived from aggregate validation outputs. Synthetic data only.", transform=ax.transAxes, fontsize=9.5, color=COLORS["gray"])
    save(fig, "cohort_attrition_flow.png")


def make_followup_curve():
    followup = read_csv(BI_DIR / "followup_timing_table.csv")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLORS["white"])
    plot_followup_curve(ax, followup, "Figure 3. Cumulative outpatient follow-up window summary")
    ax.text(
        0.0,
        -0.22,
        "Cumulative window summary based on aggregate follow-up outputs at 7, 14, and 30 days.",
        transform=ax.transAxes,
        fontsize=9,
        color=COLORS["gray"],
    )
    save(fig, "cumulative_outpatient_followup_curve.png")


def make_prior_utilization():
    prior = read_csv(ANALYSIS_DIR / "prior_utilization_group_summary.csv")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLORS["white"])
    plot_prior_utilization(ax, prior, "Figure 4. Readmission rate by prior utilization group")
    ax.text(
        0.0,
        -0.20,
        "Descriptive synthetic-data output. Prior utilization groups are based on prior encounter counts in the 12 months before index admission.",
        transform=ax.transAxes,
        fontsize=9,
        color=COLORS["gray"],
    )
    save(fig, "readmission_by_prior_utilization_group.png")


def make_forest_plot():
    reg = prepare_regression()
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=COLORS["white"])
    plot_forest(ax, reg, "Figure 5. Exploratory Logistic Regression for 30-Day Readmission", compact=False)
    ax.text(
        0.0,
        -0.18,
        "Synthetic-data demonstration only; estimates are exploratory and limited by small event count. Red marker indicates p < 0.05.",
        transform=ax.transAxes,
        fontsize=9,
        color=COLORS["gray"],
    )
    save(fig, "logistic_regression_forest_plot_professional.png")


def main():
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    make_dashboard()
    make_cohort_flow()
    make_followup_curve()
    make_prior_utilization()
    make_forest_plot()


if __name__ == "__main__":
    main()
