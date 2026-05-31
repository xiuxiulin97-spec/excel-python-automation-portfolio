from pathlib import Path

import pandas as pd

from cleaner import clean_customer_data, normalize_columns, read_customer_file


def test_read_customer_file_supports_csv(tmp_path: Path):
    file_path = tmp_path / "customers.csv"
    file_path.write_text("姓名,電話,Email,公司\n王小明,0912-345-678,test@example.com,A公司\n", encoding="utf-8-sig")

    df = read_customer_file(str(file_path))

    assert df.to_dict("records") == [
        {"姓名": "王小明", "電話": "0912-345-678", "Email": "test@example.com", "公司": "A公司"}
    ]


def test_read_customer_file_supports_excel(tmp_path: Path):
    file_path = tmp_path / "customers.xlsx"
    pd.DataFrame([{"姓名": "王小明", "電話": "0912-345-678", "Email": "test@example.com", "公司": "A公司"}]).to_excel(
        file_path, index=False, engine="openpyxl"
    )

    df = read_customer_file(str(file_path))

    assert df.to_dict("records") == [
        {"姓名": "王小明", "電話": "0912-345-678", "Email": "test@example.com", "公司": "A公司"}
    ]


def test_normalize_columns_maps_common_customer_field_names():
    df = pd.DataFrame(
        [
            {
                "客戶姓名": "王小明",
                "手機": "0912-345-678",
                "電子郵件": "TEST@EXAMPLE.COM",
                "公司名稱": "A公司",
            }
        ]
    )

    normalized = normalize_columns(df)

    assert normalized.columns.tolist() == ["姓名", "電話", "Email", "公司"]
    assert normalized.loc[0, "姓名"] == "王小明"


def test_clean_customer_data_removes_empty_rows_cleans_phone_and_deduplicates():
    df = pd.DataFrame(
        [
            {"姓名": "王小明", "電話": "0912-345-678", "Email": "test@example.com", "公司": "A公司"},
            {"姓名": None, "電話": None, "Email": None, "公司": None},
            {"姓名": "王小明", "電話": "(0912) 345 678", "Email": "test@example.com", "公司": "A公司"},
            {"姓名": "陳美華", "電話": "02-2345-6789", "Email": "chen@example.com", "公司": "B公司"},
        ]
    )

    cleaned, issues = clean_customer_data(df)

    assert cleaned.to_dict("records") == [
        {"姓名": "王小明", "電話": "0912345678", "Email": "test@example.com", "公司": "A公司"},
        {"姓名": "陳美華", "電話": "0223456789", "Email": "chen@example.com", "公司": "B公司"},
    ]
    assert issues.empty
