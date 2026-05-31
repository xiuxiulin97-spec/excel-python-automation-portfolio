import pandas as pd

from config import CLEANED_DATA_SHEET_NAME, SUMMARY_SHEET_NAME
from sheets_client import build_batch_update_payload, dataframe_to_values


def test_dataframe_to_values_includes_headers_and_rows():
    df = pd.DataFrame({"客戶": ["A公司"], "金額": [1000]})

    values = dataframe_to_values(df)

    assert values == [["客戶", "金額"], ["A公司", 1000]]


def test_dataframe_to_values_converts_empty_cells_to_blank_strings():
    df = pd.DataFrame({"客戶": ["A公司", None], "金額": [1000, None]})

    values = dataframe_to_values(df)

    assert values == [["客戶", "金額"], ["A公司", 1000.0], ["", ""]]


def test_build_batch_update_payload_contains_two_target_sheets():
    cleaned_df = pd.DataFrame({"客戶": ["A公司"], "金額": [1000]})
    summary_df = pd.DataFrame({"客戶": ["A公司"], "金額總和": [1000]})

    payload = build_batch_update_payload(cleaned_df, summary_df)

    assert payload["valueInputOption"] == "RAW"
    assert payload["data"][0]["range"] == f"{CLEANED_DATA_SHEET_NAME}!A1"
    assert payload["data"][1]["range"] == f"{SUMMARY_SHEET_NAME}!A1"
    assert payload["data"][0]["values"] == [["客戶", "金額"], ["A公司", 1000]]
    assert payload["data"][1]["values"] == [["客戶", "金額總和"], ["A公司", 1000]]
