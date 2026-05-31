from __future__ import annotations

from pathlib import Path

import pandas as pd

from validator import build_issue_report


STANDARD_COLUMNS = ["姓名", "電話", "Email", "公司"]

COLUMN_ALIASES = {
    "姓名": "姓名",
    "名字": "姓名",
    "客戶": "姓名",
    "客戶姓名": "姓名",
    "名稱": "姓名",
    "name": "姓名",
    "customer": "姓名",
    "customer_name": "姓名",
    "電話": "電話",
    "手機": "電話",
    "聯絡電話": "電話",
    "行動電話": "電話",
    "phone": "電話",
    "mobile": "電話",
    "tel": "電話",
    "email": "Email",
    "e-mail": "Email",
    "mail": "Email",
    "電子郵件": "Email",
    "信箱": "Email",
    "Email": "Email",
    "公司": "公司",
    "公司名稱": "公司",
    "company": "公司",
}


def read_customer_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        try:
            return pd.read_csv(path, dtype=str, encoding="utf-8-sig")
        except UnicodeDecodeError:
            return pd.read_csv(path, dtype=str, encoding="cp950")

    if suffix in {".xlsx", ".xlsm"}:
        return pd.read_excel(path, sheet_name=0, dtype=str, engine="openpyxl")

    raise ValueError("只支援 Excel (.xlsx, .xlsm) 或 CSV (.csv) 檔案。")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed_df = df.copy()
    renamed_df.columns = [_normalize_column_name(column) for column in renamed_df.columns]

    normalized_df = pd.DataFrame(index=renamed_df.index)
    for column in STANDARD_COLUMNS:
        matching_columns = renamed_df.loc[:, renamed_df.columns == column]
        if matching_columns.empty:
            normalized_df[column] = ""
        else:
            normalized_df[column] = matching_columns.bfill(axis=1).iloc[:, 0]

    return normalized_df[STANDARD_COLUMNS]


def clean_customer_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    normalized_df = normalize_columns(df)
    normalized_df = normalized_df.map(_clean_cell)
    normalized_df = normalized_df.replace("", pd.NA).dropna(how="all").fillna("")

    normalized_df["電話"] = normalized_df["電話"].map(clean_phone)
    normalized_df["Email"] = normalized_df["Email"].map(lambda value: str(value).strip().lower())

    issues_df = build_issue_report(normalized_df)
    issue_indexes = set(issues_df["_source_index"].tolist()) if not issues_df.empty else set()

    cleaned_df = normalized_df.loc[~normalized_df.index.isin(issue_indexes)].copy()
    cleaned_df = cleaned_df.drop_duplicates(subset=["姓名", "電話", "Email"], keep="first")
    cleaned_df = cleaned_df.reset_index(drop=True)

    public_issues_df = issues_df.drop(columns=["_source_index"], errors="ignore").reset_index(drop=True)
    return cleaned_df, public_issues_df


def clean_phone(phone: str) -> str:
    return "".join(character for character in str(phone) if character.isdigit())


def _normalize_column_name(column: object) -> str:
    column_text = str(column).strip()
    return COLUMN_ALIASES.get(column_text, COLUMN_ALIASES.get(column_text.lower(), column_text))


def _clean_cell(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()
