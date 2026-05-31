import pandas as pd

from cleaner import clean_data, read_source_file


def test_clean_data_removes_fully_blank_rows():
    df = pd.DataFrame(
        {
            "客戶": ["A公司", None, "B公司", "   "],
            "金額": [1000, None, 2000, "   "],
        }
    )

    cleaned_df = clean_data(df)

    assert len(cleaned_df) == 2
    assert cleaned_df["客戶"].tolist() == ["A公司", "B公司"]


def test_clean_data_removes_exact_duplicates():
    df = pd.DataFrame(
        {
            "客戶": ["A公司", "A公司", "B公司"],
            "金額": [1000, 1000, 2000],
        }
    )

    cleaned_df = clean_data(df)

    assert len(cleaned_df) == 2


def test_read_source_file_reads_csv(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text("客戶,金額\nA公司,1000\nB公司,2000\n", encoding="utf-8")

    df = read_source_file(str(csv_path))

    assert df.shape == (2, 2)
    assert df.loc[0, "客戶"] == "A公司"


def test_read_source_file_reads_first_excel_sheet(tmp_path):
    excel_path = tmp_path / "sales.xlsx"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        pd.DataFrame({"客戶": ["A公司"], "金額": [1000]}).to_excel(
            writer, index=False, sheet_name="第一張"
        )
        pd.DataFrame({"客戶": ["B公司"], "金額": [9999]}).to_excel(
            writer, index=False, sheet_name="第二張"
        )

    df = read_source_file(str(excel_path))

    assert df.loc[0, "客戶"] == "A公司"
    assert df.loc[0, "金額"] == 1000
