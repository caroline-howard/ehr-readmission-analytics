from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy import stats


def wilson_ci(count: int, n: int, confidence: float = 0.95) -> tuple[float, float]:
    """Return Wilson score confidence interval bounds as proportions."""
    if n <= 0:
        return (math.nan, math.nan)

    p_hat = count / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    denominator = 1 + (z**2 / n)
    center = (p_hat + (z**2 / (2 * n))) / denominator
    margin = (
        z
        * math.sqrt((p_hat * (1 - p_hat) / n) + (z**2 / (4 * n**2)))
        / denominator
    )
    return (max(0.0, center - margin), min(1.0, center + margin))


def choose_subgroup_test(contingency_table: Any) -> dict[str, Any]:
    """Choose Fisher's exact test for sparse 2x2 tables, otherwise chi-square."""
    table = np.asarray(contingency_table, dtype=float)
    if table.ndim != 2 or table.shape[0] < 2 or table.shape[1] < 2:
        raise ValueError("contingency_table must be a 2D table with at least 2 rows and 2 columns")

    chi2, chi_p, _, expected = stats.chi2_contingency(table, correction=False)
    has_sparse_expected_cell = bool(np.any(expected < 5))

    if has_sparse_expected_cell and table.shape == (2, 2):
        _, fisher_p = stats.fisher_exact(table)
        return {
            "test_name": "Fisher's exact test",
            "p_value": float(fisher_p),
            "expected_counts": expected,
            "reason": "At least one expected cell count was < 5.",
        }

    return {
        "test_name": "Chi-square test of independence",
        "p_value": float(chi_p),
        "expected_counts": expected,
        "reason": "All expected cell counts were >= 5."
        if not has_sparse_expected_cell
        else "Sparse expected cells present, but table is not 2x2; chi-square reported cautiously.",
    }


def format_p_value(p: float | None) -> str:
    if p is None or math.isnan(p):
        return "Not calculated"
    if p < 0.001:
        return "<0.001"
    return f"{p:.3f}"


def subgroup_size_note(n: int) -> str:
    if n < 30:
        return "Small subgroup; rate should be interpreted cautiously."
    return "Subgroup size >= 30; still descriptive and exploratory."
