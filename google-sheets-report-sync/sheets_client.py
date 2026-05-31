from datetime import date, datetime
from typing import Any

import pandas as pd

from config import CLEANED_DATA_SHEET_NAME, SUMMARY_SHEET_NAME


def normalize_cell_value(value: Any) -> Any:
    if pd.isna(value):
        return ""

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if hasattr(value, "item"):
        return value.item()

    return value


def dataframe_to_values(df: pd.DataFrame) -> list[list[Any]]:
    if df.empty and len(df.columns) == 0:
        return []

    headers = [str(column) for column in df.columns]
    rows = [
        [normalize_cell_value(value) for value in row]
        for row in df.itertuples(index=False, name=None)
    ]

    return [headers, *rows]


def build_batch_update_payload(
    cleaned_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    value_input_option: str = "RAW",
) -> dict[str, Any]:
    return {
        "valueInputOption": value_input_option,
        "data": [
            {
                "range": f"{CLEANED_DATA_SHEET_NAME}!A1",
                "values": dataframe_to_values(cleaned_df),
            },
            {
                "range": f"{SUMMARY_SHEET_NAME}!A1",
                "values": dataframe_to_values(summary_df),
            },
        ],
    }
