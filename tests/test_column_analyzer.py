from pathlib import Path

import pandas as pd

from column_analyzer import analyze_columns
from reader import read_table


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def analysis_by_name(df):
    return {item["name"]: item for item in analyze_columns(df)}


def test_analyze_sales_data_columns():
    df = read_table(FIXTURES_DIR / "sales_data.csv")

    result = analysis_by_name(df)

    assert result["客戶"]["type"] == "text"
    assert result["金額"]["type"] == "number"
    assert result["日期"]["type"] == "date"
    assert result["產品"]["type"] == "text"


def test_analyze_customer_data_columns():
    df = read_table(FIXTURES_DIR / "customer_data.csv")

    result = analysis_by_name(df)

    assert result["姓名"]["type"] == "text"
    assert result["電話"]["type"] == "text"
    assert result["Email"]["type"] == "text"
    assert result["公司"]["type"] == "text"


def test_analyze_medical_agent_data_columns():
    df = read_table(FIXTURES_DIR / "medical_agent_data.csv")

    result = analysis_by_name(df)

    assert result["姓名"]["type"] == "text"
    assert result["醫院名稱"]["type"] == "text"
    assert result["代理人"]["type"] == "text"
    assert result["項目金額"]["type"] == "number"
    assert result["金額"]["type"] == "number"
    assert result["手術日期"]["type"] == "date"


def test_analyze_columns_returns_examples_and_counts():
    df = pd.DataFrame(
        [
            {"姓名": "王小明", "金額": 1000, "日期": "2026-01-01"},
            {"姓名": "李小美", "金額": 2000, "日期": "2026-01-02"},
        ]
    )

    result = analysis_by_name(df)

    assert result["姓名"]["non_null_count"] == 2
    assert result["姓名"]["sample_values"] == ["王小明", "李小美"]
    assert result["金額"]["sample_values"] == ["1000", "2000"]


def test_empty_column_defaults_to_text():
    df = pd.DataFrame({"備註": [None, None]})

    result = analyze_columns(df)

    assert result == [
        {
            "name": "備註",
            "type": "text",
            "non_null_count": 0,
            "sample_values": [],
        }
    ]
