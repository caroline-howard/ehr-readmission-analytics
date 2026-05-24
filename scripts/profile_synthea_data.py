"""Profile local Synthea CSV extracts before writing cohort SQL.

This script is intentionally lightweight. It checks which expected Synthea
tables are available, prints table shapes and columns, summarizes encounter
classification values, and writes a small profiling summary when local data are
present. Profiling comes before cohort SQL so encounter classes, date fields,
and missingness can be validated against the actual export.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("outputs")

EXPECTED_FILES = [
    "patients.csv",
    "encounters.csv",
    "conditions.csv",
    "observations.csv",
    "medications.csv",
    "payers.csv",
    "payer_transitions.csv",
]

REQUIRED_FILES = ["patients.csv", "encounters.csv"]
CORE_TABLES = ["patients", "encounters", "conditions"]


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with lowercase snake_case-like column names."""
    renamed = {
        col: str(col).strip().lower().replace(" ", "_").replace("-", "_")
        for col in df.columns
    }
    return df.rename(columns=renamed)


def load_available_tables(raw_dir: Path) -> dict[str, pd.DataFrame]:
    """Load expected Synthea CSV files that are present in the raw folder."""
    tables: dict[str, pd.DataFrame] = {}
    for filename in EXPECTED_FILES:
        path = raw_dir / filename
        if path.exists():
            table_name = path.stem
            try:
                tables[table_name] = standardize_columns(pd.read_csv(path, low_memory=False))
            except Exception as exc:
                print(f"ERROR: Could not read {path}: {exc}")
    return tables


def summarize_missingness(df: pd.DataFrame, table_name: str) -> list[dict[str, object]]:
    """Summarize missingness for each column in a table."""
    rows = []
    row_count = len(df)
    for column in df.columns:
        missing_count = int(df[column].isna().sum())
        rows.append(
            {
                "table": table_name,
                "column": column,
                "row_count": row_count,
                "missing_count": missing_count,
                "missing_percent": round((missing_count / row_count) * 100, 2)
                if row_count
                else 0.0,
            }
        )
    return rows


def summarize_date_fields(df: pd.DataFrame, table_name: str) -> list[dict[str, object]]:
    """Summarize likely date fields without assuming exact Synthea schemas."""
    rows = []
    date_like_columns = [
        col
        for col in df.columns
        if any(token in col.lower() for token in ["date", "birth", "death", "start", "stop"])
    ]
    for column in date_like_columns:
        parsed = pd.to_datetime(df[column], errors="coerce")
        rows.append(
            {
                "table": table_name,
                "column": column,
                "non_missing_dates": int(parsed.notna().sum()),
                "min_date": parsed.min(),
                "max_date": parsed.max(),
            }
        )
    return rows


def print_file_inventory(raw_dir: Path) -> None:
    """Print expected Synthea file availability."""
    print("Synthea CSV file inventory")
    print("==========================")
    for filename in EXPECTED_FILES:
        status = "present" if (raw_dir / filename).exists() else "missing"
        print(f"- {filename}: {status}")

    missing_required = [name for name in REQUIRED_FILES if not (raw_dir / name).exists()]
    if missing_required:
        print()
        print("ERROR: Required files are missing for core profiling:")
        for filename in missing_required:
            print(f"- {filename}")
        print("Place Synthea CSV files in data/raw/ before cohort construction.")


def print_table_profiles(tables: dict[str, pd.DataFrame]) -> None:
    """Print shapes, columns, previews, and encounter class values."""
    print()
    print("Loaded table profiles")
    print("=====================")
    if not tables:
        print("No expected Synthea CSV files were loaded.")
        return

    for table_name, df in tables.items():
        print()
        print(f"{table_name}")
        print("-" * len(table_name))
        print(f"shape: {df.shape[0]} rows x {df.shape[1]} columns")
        print("columns:", ", ".join(df.columns))

    for table_name in CORE_TABLES:
        if table_name in tables:
            print()
            print(f"Preview: {table_name}")
            print(tables[table_name].head().to_string(index=False))

    encounters = tables.get("encounters")
    if encounters is not None:
        class_columns = [
            col
            for col in encounters.columns
            if col in {"encounterclass", "encounter_class", "class", "type"}
            or "class" in col.lower()
            or "type" in col.lower()
        ]
        print()
        print("Encounter class/type values")
        print("===========================")
        if not class_columns:
            print("No obvious encounter class/type columns found.")
        for column in class_columns:
            print()
            print(f"{column}:")
            print(encounters[column].value_counts(dropna=False).head(20).to_string())


def write_profile_summary(tables: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Write a compact profiling summary for reproducible review."""
    if not tables:
        print()
        print("No profiling summary written because no expected CSV files were loaded.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for table_name, df in tables.items():
        rows.append(
            {
                "summary_type": "table_shape",
                "table": table_name,
                "column": None,
                "value": f"{df.shape[0]} rows x {df.shape[1]} columns",
            }
        )
        for item in summarize_missingness(df, table_name):
            rows.append(
                {
                    "summary_type": "missingness",
                    "table": item["table"],
                    "column": item["column"],
                    "value": f"{item['missing_count']} missing ({item['missing_percent']}%)",
                }
            )
        for item in summarize_date_fields(df, table_name):
            rows.append(
                {
                    "summary_type": "date_range",
                    "table": item["table"],
                    "column": item["column"],
                    "value": f"{item['non_missing_dates']} parsed dates; {item['min_date']} to {item['max_date']}",
                }
            )

    output_path = output_dir / "data_profile_summary.csv"
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print()
    print(f"Wrote profiling summary to {output_path}")


def main() -> None:
    print_file_inventory(RAW_DIR)
    tables = load_available_tables(RAW_DIR)
    print_table_profiles(tables)
    write_profile_summary(tables, OUTPUT_DIR)


if __name__ == "__main__":
    main()
