import gradio as gr


PROJECT_DESCRIPTION = """
This portfolio project demonstrates an end-to-end retrospective healthcare
research analytics workflow for 30-day hospital readmission using Synthea
synthetic EHR data.

The current version is a placeholder for project presentation only. It does
not contain real patient data, analysis outputs, or model results.
"""


def build_app() -> gr.Blocks:
    with gr.Blocks(title="EHR Readmission Analytics") as demo:
        gr.Markdown("# EHR Readmission Analytics")
        gr.Markdown(PROJECT_DESCRIPTION)
    return demo


if __name__ == "__main__":
    build_app().launch()
