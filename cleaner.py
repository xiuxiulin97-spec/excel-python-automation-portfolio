from __future__ import annotations

import pandas as pd


def read_excel(file_path: str) -> pd.DataFrame:
    """Read the first worksheet from an Excel workbook."""
    return pd.read_excel(file_path, sheet_name=0, engine="openpyxl")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove fully empty rows and exact duplicate rows."""
    return df.dropna(how="all").drop_duplicates().reset_index(drop=True)
