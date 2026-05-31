from pathlib import Path

import pandas as pd

from config import SUPPORTED_CSV_EXTENSIONS, SUPPORTED_EXCEL_EXTENSIONS


def read_source_file(file_path: str) -> pd.DataFrame:
    """Read the selected Excel or CSV file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"找不到檔案：{file_path}")

    suffix = path.suffix.lower()

    if suffix in SUPPORTED_CSV_EXTENSIONS:
        return pd.read_csv(path)

    if suffix in SUPPORTED_EXCEL_EXTENSIONS:
        return pd.read_excel(path, sheet_name=0, engine="openpyxl")

    raise ValueError("只支援 Excel (.xlsx, .xlsm) 或 CSV (.csv) 檔案")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove fully blank rows and exact duplicate records."""
    cleaned_df = df.copy()
    cleaned_df = cleaned_df.replace(r"^\s*$", pd.NA, regex=True)
    cleaned_df = cleaned_df.dropna(how="all")
    cleaned_df = cleaned_df.drop_duplicates()
    return cleaned_df.reset_index(drop=True)
