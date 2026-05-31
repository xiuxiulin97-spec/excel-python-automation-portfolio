from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = ("客戶", "金額")


def validate_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        missing_text = "、".join(missing_columns)
        raise ValueError(f"Excel 缺少必要欄位：{missing_text}")


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)

    working_df = df.copy()
    working_df["金額"] = pd.to_numeric(working_df["金額"], errors="coerce")

    invalid_amount_count = working_df["金額"].isna().sum()
    if invalid_amount_count:
        raise ValueError("金額欄位包含無法轉換成數字的資料，請檢查 Excel 內容。")

    summary_df = (
        working_df.groupby("客戶", as_index=False, sort=True)["金額"]
        .sum()
        .rename(columns={"金額": "金額總和"})
    )
    return summary_df


def export_report(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
    output_dir: str = "output",
) -> str:
    summary_df = build_summary(cleaned_df)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_path / f"result_{timestamp}.xlsx"

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        original_df.to_excel(writer, sheet_name="原始資料", index=False)
        cleaned_df.to_excel(writer, sheet_name="清理後資料", index=False)
        summary_df.to_excel(writer, sheet_name="統計報表", index=False)

    return str(report_path)
