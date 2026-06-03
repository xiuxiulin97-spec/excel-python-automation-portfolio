from __future__ import annotations

from typing import Any

import pandas as pd

from value_parser import parse_amount_series


TEXT = "text"
NUMBER = "number"
DATE = "date"
DEFAULT_THRESHOLD = 0.8
DATE_KEYWORDS = ("日期", "日付", "date", "時間", "時间", "time")


def analyze_columns(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Analyze DataFrame columns for future GUI field selection."""
    results: list[dict[str, Any]] = []

    for column in df.columns:
        series = df[column]
        non_empty = _non_empty_values(series)
        column_type = infer_column_type(series, column_name=str(column), threshold=DEFAULT_THRESHOLD)

        results.append(
            {
                "name": str(column),
                "type": column_type,
                "non_null_count": int(len(non_empty)),
                "sample_values": _sample_values(non_empty),
            }
        )

    return results


def infer_column_type(
    series: pd.Series,
    column_name: str = "",
    threshold: float = DEFAULT_THRESHOLD,
) -> str:
    non_empty = _non_empty_values(series)
    if non_empty.empty:
        return TEXT

    if pd.api.types.is_datetime64_any_dtype(series):
        return DATE

    if _is_date_like_column(column_name) and _excel_serial_date_ratio(non_empty) >= threshold:
        return DATE

    if pd.api.types.is_numeric_dtype(series):
        return NUMBER

    if _date_ratio(non_empty) >= threshold:
        return DATE

    if _number_ratio(non_empty) >= threshold:
        return NUMBER

    return TEXT


def _non_empty_values(series: pd.Series) -> pd.Series:
    if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
        series = series.replace(r"^\s*$", pd.NA, regex=True)
    return series.dropna()


def _number_ratio(series: pd.Series) -> float:
    converted = parse_amount_series(series)
    return float(converted.notna().mean())


def _date_ratio(series: pd.Series) -> float:
    if _number_ratio(series) >= DEFAULT_THRESHOLD:
        return 0.0

    converted = pd.to_datetime(series, errors="coerce", format="mixed")
    return float(converted.notna().mean())


def _excel_serial_date_ratio(series: pd.Series) -> float:
    converted = pd.to_numeric(series, errors="coerce")
    valid = converted.dropna()
    if valid.empty:
        return 0.0
    return float(valid.between(20000, 80000).mean())


def _is_date_like_column(column_name: str) -> bool:
    normalized = column_name.strip().lower()
    return any(keyword.lower() in normalized for keyword in DATE_KEYWORDS)


def _sample_values(series: pd.Series, limit: int = 3) -> list[str]:
    return [str(value) for value in series.head(limit).tolist()]
