import pandas as pd
import pytest

from config import CLEANED_DATA_SHEET_NAME, SUMMARY_SHEET_NAME
from sheets_client import (
    build_add_sheet_requests,
    build_batch_update_payload,
    dataframe_to_values,
    write_report_to_google_sheets,
)


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


def test_build_add_sheet_requests_only_adds_missing_sheets():
    requests = build_add_sheet_requests({CLEANED_DATA_SHEET_NAME})

    assert requests == [{"addSheet": {"properties": {"title": SUMMARY_SHEET_NAME}}}]


def test_write_report_to_google_sheets_raises_when_sheet_id_is_blank():
    cleaned_df = pd.DataFrame({"客戶": ["A公司"], "金額": [1000]})
    summary_df = pd.DataFrame({"客戶": ["A公司"], "金額總和": [1000]})

    with pytest.raises(ValueError, match="請輸入 Google Sheet ID"):
        write_report_to_google_sheets("   ", cleaned_df, summary_df, service=FakeSheetsService())


def test_write_report_to_google_sheets_uses_expected_api_calls():
    service = FakeSheetsService(existing_sheet_names={"清理後資料"})
    cleaned_df = pd.DataFrame({"客戶": ["A公司"], "金額": [1000]})
    summary_df = pd.DataFrame({"客戶": ["A公司"], "金額總和": [1000]})

    response = write_report_to_google_sheets("sheet-123", cleaned_df, summary_df, service=service)

    assert response == {"updatedRanges": ["清理後資料!A1", "統計報表!A1"]}
    assert service.get_called_with == "sheet-123"
    assert service.batch_update_body == {
        "requests": [{"addSheet": {"properties": {"title": "統計報表"}}}]
    }
    assert service.batch_clear_body == {"ranges": ["清理後資料", "統計報表"]}
    assert service.values_batch_update_body["data"][0]["range"] == "清理後資料!A1"
    assert service.values_batch_update_body["data"][1]["range"] == "統計報表!A1"


class FakeExecutable:
    def __init__(self, response):
        self.response = response

    def execute(self):
        return self.response


class FakeValuesResource:
    def __init__(self, service):
        self.service = service

    def batchClear(self, spreadsheetId, body):
        self.service.batch_clear_spreadsheet_id = spreadsheetId
        self.service.batch_clear_body = body
        return FakeExecutable({})

    def batchUpdate(self, spreadsheetId, body):
        self.service.values_batch_update_spreadsheet_id = spreadsheetId
        self.service.values_batch_update_body = body
        return FakeExecutable(
            {"updatedRanges": [item["range"] for item in body.get("data", [])]}
        )


class FakeSpreadsheetsResource:
    def __init__(self, service):
        self.service = service

    def get(self, spreadsheetId):
        self.service.get_called_with = spreadsheetId
        sheets = [
            {"properties": {"title": sheet_name}}
            for sheet_name in self.service.existing_sheet_names
        ]
        return FakeExecutable({"sheets": sheets})

    def batchUpdate(self, spreadsheetId, body):
        self.service.batch_update_spreadsheet_id = spreadsheetId
        self.service.batch_update_body = body
        return FakeExecutable({})

    def values(self):
        return FakeValuesResource(self.service)


class FakeSheetsService:
    def __init__(self, existing_sheet_names=None):
        self.existing_sheet_names = existing_sheet_names or set()
        self.get_called_with = None
        self.batch_update_body = None
        self.batch_clear_body = None
        self.values_batch_update_body = None

    def spreadsheets(self):
        return FakeSpreadsheetsResource(self)
