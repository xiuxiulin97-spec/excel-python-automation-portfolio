from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


def export_customer_report(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
    issues_df: pd.DataFrame,
    output_dir: str = "output",
) -> str:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_path / f"cleaned_customers_{timestamp}.xlsx"

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        original_df.to_excel(writer, sheet_name="原始資料", index=False)
        cleaned_df.to_excel(writer, sheet_name="清理後資料", index=False)
        issues_df.to_excel(writer, sheet_name="問題資料", index=False)

    return str(report_path)
