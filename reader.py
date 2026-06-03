from __future__ import annotations

from pathlib import Path
from typing import Any, Union

import pandas as pd


PathLike = Union[str, Path]
EXCEL_EXTENSIONS = {".xlsx", ".xlsm"}
CSV_EXTENSIONS = {".csv"}
HEADER_SCAN_ROWS = 10


def read_table(file_path: PathLike) -> pd.DataFrame:
    """Read an Excel or CSV file into a DataFrame.

    Excel files always read the first worksheet. The reader also handles common
    business spreadsheets where the first row is a title and the real header
    appears a few rows below.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"找不到檔案：{path}")

    suffix = path.suffix.lower()
    if suffix in EXCEL_EXTENSIONS:
        raw_df = pd.read_excel(path, sheet_name=0, engine="openpyxl", header=None)
        return _normalize_table(raw_df)

    if suffix in CSV_EXTENSIONS:
        return _read_csv_with_fallback(path)

    supported = ", ".join(sorted(EXCEL_EXTENSIONS | CSV_EXTENSIONS))
    raise ValueError(f"不支援的檔案格式：{suffix}。支援格式：{supported}")


def _read_csv_with_fallback(path: Path) -> pd.DataFrame:
    encodings = ("utf-8-sig", "utf-8", "cp950")
    last_error: UnicodeDecodeError | None = None

    for encoding in encodings:
        try:
            raw_df = pd.read_csv(path, encoding=encoding, header=None)
            return _normalize_table(raw_df)
        except UnicodeDecodeError as exc:
            last_error = exc

    raise ValueError(f"無法讀取 CSV 編碼：{path}") from last_error


def _normalize_table(raw_df: pd.DataFrame) -> pd.DataFrame:
    working_df = raw_df.dropna(how="all").reset_index(drop=True)
    if working_df.empty:
        return pd.DataFrame()

    header_index = _detect_header_row(working_df)
    columns = _build_column_names(working_df.iloc[header_index].tolist())
    data_df = working_df.iloc[header_index + 1 :].copy()
    data_df.columns = columns

    return data_df.dropna(how="all").reset_index(drop=True)


def _detect_header_row(df: pd.DataFrame) -> int:
    scan_count = min(len(df), HEADER_SCAN_ROWS)
    best_index = 0
    best_score = float("-inf")

    for index in range(scan_count):
        row = df.iloc[index].tolist()
        next_row = df.iloc[index + 1].tolist() if index + 1 < len(df) else []
        score = _header_score(row, next_row, total_columns=len(df.columns))
        if score > best_score:
            best_score = score
            best_index = index

    return best_index


def _header_score(row: list[Any], next_row: list[Any], total_columns: int) -> float:
    values = [_clean_cell(value) for value in row]
    non_empty = [value for value in values if value]
    if not non_empty:
        return float("-inf")

    next_non_empty_count = sum(1 for value in next_row if _clean_cell(value))
    numeric_count = sum(1 for value in non_empty if _looks_numeric(value))
    date_count = sum(1 for value in non_empty if _looks_date(value))
    text_count = len(non_empty) - numeric_count - date_count

    score = len(non_empty) * 3
    score += text_count * 2
    score -= numeric_count * 2
    score -= date_count * 2

    if next_non_empty_count >= max(2, len(non_empty) // 2):
        score += 4

    if len(non_empty) == 1 and total_columns > 2:
        score -= 8

    return score


def _build_column_names(values: list[Any]) -> list[str]:
    columns: list[str] = []
    seen: dict[str, int] = {}

    for index, value in enumerate(values, start=1):
        column = _clean_cell(value)
        if not column or column.lower().startswith("unnamed"):
            column = f"欄位{index}"

        count = seen.get(column, 0) + 1
        seen[column] = count
        if count > 1:
            column = f"{column}_{count}"

        columns.append(column)

    return columns


def _clean_cell(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def _looks_numeric(value: str) -> bool:
    return pd.to_numeric(pd.Series([value]), errors="coerce").notna().iloc[0]


def _looks_date(value: str) -> bool:
    if _looks_numeric(value):
        return False
    return pd.to_datetime(pd.Series([value]), errors="coerce", format="mixed").notna().iloc[0]
