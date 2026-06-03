from __future__ import annotations

import pandas as pd

from value_parser import parse_amount_series


def build_summary(df: pd.DataFrame, value_column: str) -> pd.DataFrame:
    """Build an overview report for the selected numeric column."""
    values = _numeric_series(df, value_column)

    return pd.DataFrame(
        [
            {"項目": "總筆數", "值": int(len(df))},
            {"項目": f"{value_column}總和", "值": _clean_number(values.sum())},
            {"項目": f"{value_column}平均值", "值": _clean_number(values.mean())},
        ]
    )


def build_group_report(
    df: pd.DataFrame,
    group_column: str,
    value_column: str | None = None,
) -> pd.DataFrame:
    """Group rows by a user-selected column and optionally aggregate a value column."""
    _validate_column(df, group_column)

    if value_column is None:
        grouped = (
            df.groupby(group_column, dropna=False, sort=True)
            .size()
            .reset_index(name="筆數")
        )
        return grouped

    working_df = df.copy()
    working_df[value_column] = _numeric_series(working_df, value_column)

    grouped = (
        working_df.groupby(group_column, dropna=False, sort=True)
        .agg(筆數=(value_column, "count"), **{
            f"{value_column}總和": (value_column, "sum"),
            f"{value_column}平均值": (value_column, "mean"),
        })
        .reset_index()
    )
    grouped = grouped[grouped["筆數"] > 0]
    grouped = grouped.sort_values(
        by=f"{value_column}總和",
        ascending=False,
        kind="mergesort",
    ).reset_index(drop=True)
    return _clean_numeric_columns(grouped)


def build_top10_report(
    df: pd.DataFrame,
    value_column: str,
    limit: int = 10,
) -> pd.DataFrame:
    """Return the top rows sorted by the selected numeric column."""
    working_df = df.copy()
    working_df[value_column] = _numeric_series(working_df, value_column)

    return (
        working_df.dropna(subset=[value_column])
        .sort_values(by=value_column, ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )


def build_monthly_report(
    df: pd.DataFrame,
    date_column: str,
    value_column: str,
) -> pd.DataFrame:
    """Aggregate the selected numeric column by month."""
    _validate_column(df, date_column)
    values = _numeric_series(df, value_column)
    dates = _date_series(df[date_column])

    working_df = pd.DataFrame(
        {
            "月份": dates.dt.to_period("M").astype("string"),
            value_column: values,
        }
    ).dropna(subset=["月份", value_column])

    result_columns = ["月份", "筆數", f"{value_column}總和", f"{value_column}平均值"]
    if working_df.empty:
        return pd.DataFrame(columns=result_columns)

    grouped = (
        working_df.groupby("月份", sort=True)
        .agg(筆數=(value_column, "size"), **{
            f"{value_column}總和": (value_column, "sum"),
            f"{value_column}平均值": (value_column, "mean"),
        })
        .reset_index()
    )
    return _clean_numeric_columns(grouped)


def _validate_column(df: pd.DataFrame, column: str) -> None:
    if column not in df.columns:
        raise ValueError(f"找不到欄位：{column}")


def _numeric_series(df: pd.DataFrame, value_column: str) -> pd.Series:
    _validate_column(df, value_column)
    converted = parse_amount_series(df[value_column])

    if converted.notna().sum() == 0:
        raise ValueError(f"統計欄位必須是數字欄位：{value_column}")

    return converted


def _date_series(series: pd.Series) -> pd.Series:
    cleaned = _blank_to_na(series)
    numeric = pd.to_numeric(cleaned, errors="coerce")

    if numeric.notna().sum() and _looks_like_excel_serial_dates(numeric.dropna()):
        return pd.to_datetime(numeric, unit="D", origin="1899-12-30", errors="coerce")

    return pd.to_datetime(cleaned, errors="coerce", format="mixed")


def _blank_to_na(series: pd.Series) -> pd.Series:
    if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
        return series.replace(r"^\s*$", pd.NA, regex=True)
    return series


def _looks_like_excel_serial_dates(series: pd.Series) -> bool:
    return bool(series.between(20000, 80000).mean() >= 0.8)


def _clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    numeric_columns = result.select_dtypes(include="number").columns
    for column in numeric_columns:
        result[column] = result[column].map(_clean_number)
    return result


def _clean_number(value: float | int) -> float | int:
    if pd.isna(value):
        return value
    float_value = float(value)
    if float_value.is_integer():
        return int(float_value)
    return float_value
