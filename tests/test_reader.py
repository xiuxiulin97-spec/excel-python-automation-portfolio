from pathlib import Path

import pandas as pd
import pytest

from reader import read_table


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_read_table_reads_csv_fixture():
    result = read_table(FIXTURES_DIR / "sales_data.csv")

    assert result.shape == (4, 4)
    assert result.columns.tolist() == ["客戶", "金額", "日期", "產品"]
    assert result.loc[0, "客戶"] == "A公司"


def test_read_table_reads_first_excel_worksheet(tmp_path):
    workbook_path = tmp_path / "multi_sheet.xlsx"
    first_sheet = pd.DataFrame([{"姓名": "王小明", "金額": 1000}])
    second_sheet = pd.DataFrame([{"姓名": "不應讀取", "金額": 9999}])

    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        first_sheet.to_excel(writer, sheet_name="第一工作表", index=False)
        second_sheet.to_excel(writer, sheet_name="第二工作表", index=False)

    result = read_table(workbook_path)

    assert result.to_dict("records") == [{"姓名": "王小明", "金額": 1000}]


def test_read_table_detects_header_after_title_row(tmp_path):
    workbook_path = tmp_path / "expense_report.xlsx"
    raw_sheet = pd.DataFrame(
        [
            ["6月16日-6月22日-報銷台賬", None, None, None, None],
            ["序号", "日期", "用途", "金額", "付款人"],
            [1, "2026-06-16", "食材", 37.49, "曾曉陽"],
            [2, "2026-06-17", "調味品", 24.6, "林秀麗"],
        ]
    )

    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        raw_sheet.to_excel(writer, sheet_name="報銷資料", index=False, header=False)

    result = read_table(workbook_path)

    assert result.columns.tolist() == ["序号", "日期", "用途", "金額", "付款人"]
    assert result.to_dict("records") == [
        {"序号": 1, "日期": "2026-06-16", "用途": "食材", "金額": 37.49, "付款人": "曾曉陽"},
        {"序号": 2, "日期": "2026-06-17", "用途": "調味品", "金額": 24.6, "付款人": "林秀麗"},
    ]


def test_read_table_supports_xlsm_extension(tmp_path):
    workbook_path = tmp_path / "macro_workbook.xlsm"
    df = pd.DataFrame([{"客戶": "A公司", "金額": 1000}])

    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="資料", index=False)

    result = read_table(workbook_path)

    assert result.to_dict("records") == [{"客戶": "A公司", "金額": 1000}]


def test_read_table_rejects_unsupported_file_type(tmp_path):
    text_path = tmp_path / "data.txt"
    text_path.write_text("not supported", encoding="utf-8")

    with pytest.raises(ValueError, match="不支援"):
        read_table(text_path)
