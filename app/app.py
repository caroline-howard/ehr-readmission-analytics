from pathlib import Path
import os
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "ehr_readmission_matplotlib")
)

import gradio as gr
import pandas as pd


OUTPUTS_DIR = PROJECT_ROOT / "outputs"
BI_DIR = OUTPUTS_DIR / "bi"
ANALYSIS_DIR = OUTPUTS_DIR / "analysis"
FIGURE_DIR = OUTPUTS_DIR / "figures"
REPORT_PATH = PROJECT_ROOT / "report" / "final_report.md"


def read_csv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame({"status": [f"Missing expected file: {path.name}"]})


def get_first_row(path: Path) -> dict:
    df = read_csv(path)
    if df.empty or "status" in df.columns:
        return {}
    return df.iloc[0].to_dict()


def metric_card(label: str, value: str, detail: str) -> str:
    return f"""
<div class="metric-card">
  <div class="metric-label">{label}</div>
  <div class="metric-value">{value}</div>
  <div class="metric-detail">{detail}</div>
</div>
"""


def build_metric_html() -> str:
    cohort = get_first_row(BI_DIR / "cohort_summary_table.csv")
    readmission = get_first_row(BI_DIR / "readmission_kpi_table.csv")
    followup = read_csv(BI_DIR / "followup_timing_table.csv")
    ed = get_first_row(BI_DIR / "ed_revisit_table.csv")

    followup_30 = {}
    if not followup.empty and "followup_window_days" in followup.columns:
        selected = followup.loc[followup["followup_window_days"] == 30]
        if not selected.empty:
            followup_30 = selected.iloc[0].to_dict()

    cards = [
        metric_card(
            "Final cohort",
            f"{int(cohort.get('cohort_patients', 0)):,}",
            "adult index hospitalizations",
        ),
        metric_card(
            "30-day readmission",
            f"{readmission.get('readmission_rate_30d_percent', 0):.1f}%",
            f"{int(readmission.get('readmitted_30d_count', 0)):,} patients",
        ),
        metric_card(
            "30-day follow-up",
            f"{followup_30.get('followup_percent', 0):.1f}%",
            f"{int(followup_30.get('followup_count', 0)):,} patients",
        ),
        metric_card(
            "30-day ED revisit",
            f"{ed.get('ed_revisit_30d_percent', 0):.1f}%",
            f"{int(ed.get('ed_revisit_30d_count', 0)):,} patients",
        ),
    ]
    return '<div class="metric-grid">' + "\n".join(cards) + "</div>"


def load_report_excerpt() -> str:
    if not REPORT_PATH.exists():
        return "Report file has not been generated yet."

    text = REPORT_PATH.read_text()
    excerpt = text.split("## Limitations")[0].strip()
    return excerpt


CUSTOM_CSS = """
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 8px 0 18px;
}
.metric-card {
  border: 1px solid #d8dee4;
  background: #ffffff;
  padding: 16px;
}
.metric-label {
  color: #5f6b76;
  font-size: 14px;
  font-weight: 700;
}
.metric-value {
  color: #1f2933;
  font-size: 34px;
  font-weight: 800;
  line-height: 1.15;
  margin-top: 8px;
}
.metric-detail {
  color: #6b7280;
  font-size: 13px;
  margin-top: 4px;
}
@media (max-width: 900px) {
  .metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 560px) {
  .metric-grid {
    grid-template-columns: 1fr;
  }
}
"""


def build_app() -> gr.Blocks:
    cohort_summary = read_csv(BI_DIR / "cohort_summary_table.csv")
    readmission_kpis = read_csv(BI_DIR / "readmission_kpi_table.csv")
    followup_summary = read_csv(BI_DIR / "followup_timing_table.csv")
    ed_summary = read_csv(BI_DIR / "ed_revisit_table.csv")
    table1 = read_csv(ANALYSIS_DIR / "table1_baseline_characteristics.csv")
    regression = read_csv(ANALYSIS_DIR / "logistic_regression_results.csv")

    with gr.Blocks(title="EHR Readmission Analytics") as demo:
        gr.HTML(f"<style>{CUSTOM_CSS}</style>")
        gr.Markdown(
            """
# Retrospective EHR Post-Discharge Utilization Analytics

Synthetic-data portfolio demo for a retrospective healthcare analytics workflow:
cohort definition, validation, post-discharge utilization tracking, dashboard-ready
KPI reporting, and exploratory readmission modeling.

This app displays aggregate outputs only. It does not contain real patient data,
patient-level synthetic records, clinical decision support, or causal claims.
"""
        )

        gr.HTML(build_metric_html())

        with gr.Tabs():
            with gr.Tab("Dashboard"):
                gr.Image(
                    value=str(FIGURE_DIR / "dashboard_mockup.png"),
                    label="Dashboard mockup",
                    height=620,
                )
                with gr.Row():
                    gr.Image(
                        value=str(FIGURE_DIR / "postdischarge_kpis.png"),
                        label="Post-discharge KPIs",
                        height=360,
                    )
                    gr.Image(
                        value=str(FIGURE_DIR / "cohort_attrition.png"),
                        label="Cohort attrition",
                        height=360,
                    )

            with gr.Tab("Aggregate Tables"):
                gr.Markdown("## BI-ready KPI tables")
                gr.Dataframe(cohort_summary, label="Cohort summary")
                gr.Dataframe(readmission_kpis, label="Readmission KPIs")
                gr.Dataframe(followup_summary, label="Outpatient follow-up timing")
                gr.Dataframe(ed_summary, label="ED revisit summary")

            with gr.Tab("Analysis"):
                gr.Markdown("## Table 1 and exploratory model outputs")
                gr.Dataframe(table1, label="Table 1 baseline characteristics")
                gr.Dataframe(regression, label="Exploratory logistic regression")
                gr.Image(
                    value=str(FIGURE_DIR / "logistic_regression_odds_ratios.png"),
                    label="Odds ratio plot",
                    height=520,
                )

            with gr.Tab("Report"):
                gr.Markdown(load_report_excerpt())
                gr.Markdown(
                    """
## Repository Links

- Main README: `README.md`
- Final report: `report/final_report.md`
- Reproducibility guide: `docs/07_reproducibility_guide.md`
- Portfolio summary: `docs/08_portfolio_summary.md`
"""
                )

    return demo


if __name__ == "__main__":
    build_app().launch()
