from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from config import (
    CLEANED_DATA_SHEET_NAME,
    CREDENTIALS_FILE,
    SCOPES,
    SUMMARY_SHEET_NAME,
    TOKEN_FILE,
)


def load_credentials(
    credentials_file: str = CREDENTIALS_FILE,
    token_file: str = TOKEN_FILE,
):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    credentials_path = Path(credentials_file)
    token_path = Path(token_file)
    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if not credentials_path.exists():
            raise FileNotFoundError(
                f"找不到 {credentials_file}，請先從 Google Cloud Console 下載 OAuth 憑證"
            )
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
        creds = flow.run_local_server(port=0)

    token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def build_sheets_service(credentials_file: str = CREDENTIALS_FILE, token_file: str = TOKEN_FILE):
    from googleapiclient.discovery import build

    creds = load_credentials(credentials_file=credentials_file, token_file=token_file)
    return build("sheets", "v4", credentials=creds)


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


def get_existing_sheet_names(service: Any, spreadsheet_id: str) -> set[str]:
    response = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = response.get("sheets", [])
    return {
        sheet.get("properties", {}).get("title", "")
        for sheet in sheets
        if sheet.get("properties", {}).get("title")
    }


def build_add_sheet_requests(existing_sheet_names: set[str]) -> list[dict[str, Any]]:
    requests = []

    for sheet_name in (CLEANED_DATA_SHEET_NAME, SUMMARY_SHEET_NAME):
        if sheet_name not in existing_sheet_names:
            requests.append({"addSheet": {"properties": {"title": sheet_name}}})

    return requests


def ensure_target_sheets(service: Any, spreadsheet_id: str) -> None:
    existing_sheet_names = get_existing_sheet_names(service, spreadsheet_id)
    requests = build_add_sheet_requests(existing_sheet_names)

    if not requests:
        return

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests},
    ).execute()


def clear_target_sheets(service: Any, spreadsheet_id: str) -> None:
    ranges = [CLEANED_DATA_SHEET_NAME, SUMMARY_SHEET_NAME]
    service.spreadsheets().values().batchClear(
        spreadsheetId=spreadsheet_id,
        body={"ranges": ranges},
    ).execute()


def write_report_to_google_sheets(
    spreadsheet_id: str,
    cleaned_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    service: Any | None = None,
) -> dict[str, Any]:
    if not spreadsheet_id.strip():
        raise ValueError("請輸入 Google Sheet ID")

    sheets_service = service or build_sheets_service()
    ensure_target_sheets(sheets_service, spreadsheet_id)
    clear_target_sheets(sheets_service, spreadsheet_id)
    payload = build_batch_update_payload(cleaned_df, summary_df)

    return (
        sheets_service.spreadsheets()
        .values()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=payload)
        .execute()
    )
