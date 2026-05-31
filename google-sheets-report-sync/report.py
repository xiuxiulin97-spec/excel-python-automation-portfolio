import pandas as pd

from config import REQUIRED_COLUMNS


def validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        missing_text = "、".join(missing_columns)
        raise ValueError(f"缺少必要欄位：{missing_text}")


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    validate_required_columns(df)

    working_df = df.copy()
    amount_series = pd.to_numeric(working_df["金額"], errors="coerce")
    raw_amount = working_df["金額"]
    invalid_amount = amount_series.isna() & raw_amount.notna() & raw_amount.astype(str).str.strip().ne("")

    if invalid_amount.any():
        raise ValueError("金額欄位包含無法轉換成數字的資料")

    working_df["金額"] = amount_series.fillna(0)

    summary_df = (
        working_df.groupby("客戶", dropna=False, as_index=False)["金額"]
        .sum()
        .rename(columns={"金額": "金額總和"})
    )

    return summary_df
