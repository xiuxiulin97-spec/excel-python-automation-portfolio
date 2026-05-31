import pandas as pd

from cleaner import clean_data, read_excel


def test_read_excel_reads_first_worksheet(tmp_path):
    workbook_path = tmp_path / "sales.xlsx"
    first_sheet = pd.DataFrame([{"客戶": "A 公司", "金額": 100}])
    second_sheet = pd.DataFrame([{"客戶": "B 公司", "金額": 999}])

    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        first_sheet.to_excel(writer, sheet_name="第一張", index=False)
        second_sheet.to_excel(writer, sheet_name="第二張", index=False)

    result = read_excel(str(workbook_path))

    assert result.to_dict("records") == [{"客戶": "A 公司", "金額": 100}]


def test_clean_data_removes_empty_rows():
    df = pd.DataFrame(
        [
            {"客戶": "A 公司", "金額": 100},
            {"客戶": None, "金額": None},
            {"客戶": "B 公司", "金額": 200},
        ]
    )

    cleaned = clean_data(df)

    assert len(cleaned) == 2
    assert cleaned["客戶"].tolist() == ["A 公司", "B 公司"]


def test_clean_data_removes_duplicate_rows():
    df = pd.DataFrame(
        [
            {"客戶": "A 公司", "金額": 100, "品項": "服務費"},
            {"客戶": "A 公司", "金額": 100, "品項": "服務費"},
            {"客戶": "A 公司", "金額": 300, "品項": "顧問費"},
        ]
    )

    cleaned = clean_data(df)

    assert len(cleaned) == 2
    assert cleaned["金額"].tolist() == [100, 300]
