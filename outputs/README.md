# Outputs

This folder is reserved for generated project artifacts such as cohort count tables, validation summaries, figures, and model outputs.

Generated files are ignored by default to avoid committing large artifacts, raw data extracts, or premature results. Profiling outputs such as `data_profile_summary.csv` are reproducible from local runs of the notebook or command-line profiling script and should not be committed unless intentionally included as a small portfolio artifact.

Raw Synthea CSV files remain outside version control in `data/raw/`. Processed data and local database files should also remain outside version control.
