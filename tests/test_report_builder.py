from pathlib import Path

import pandas as pd
import pytest

from reader import read_table
from report_builder import (
    build_group_report,
    build_monthly_report,
    build_summary,
    build_top10_report,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_build_summary_with_sales_data():
    df = read_table(FIXTURES_DIR / "sales_data.csv")

    summary = build_summary(df, value_column="金額")

    assert summary.to_dict("records") == [
        {"項目": "總筆數", "值": 4},
        {"項目": "金額總和", "值": 7500},
        {"項目": "金額平均值", "值": 1875},
    ]


def test_build_group_report_with_sales_data():
    df = read_table(FIXTURES_DIR / "sales_data.csv")

    report = build_group_report(df, group_column="客戶", value_column="金額")

    assert report.to_dict("records") == [
        {"客戶": "A公司", "筆數": 2, "金額總和": 4000, "金額平均值": 2000},
        {"客戶": "B公司", "筆數": 1, "金額總和": 2000, "金額平均值": 2000},
        {"客戶": "C公司", "筆數": 1, "金額總和": 1500, "金額平均值": 1500},
    ]


def test_build_top10_report_with_sales_data():
    df = read_table(FIXTURES_DIR / "sales_data.csv")

    report = build_top10_report(df, value_column="金額")

    assert report["金額"].tolist() == [3000, 2000, 1500, 1000]
    assert len(report) == 4


def test_build_monthly_report_with_sales_data():
    df = read_table(FIXTURES_DIR / "sales_data.csv")

    report = build_monthly_report(df, date_column="日期", value_column="金額")

    assert report.to_dict("records") == [
        {"月份": "2026-05", "筆數": 4, "金額總和": 7500, "金額平均值": 1875}
    ]


def test_report_builder_supports_customer_data_without_date_or_numeric_fields():
    df = read_table(FIXTURES_DIR / "customer_data.csv")

    group_report = build_group_report(df, group_column="公司")

    assert group_report.to_dict("records") == [
        {"公司": "A公司", "筆數": 1},
        {"公司": "B公司", "筆數": 1},
        {"公司": "C公司", "筆數": 1},
    ]

    with pytest.raises(ValueError, match="統計欄位"):
        build_summary(df, value_column="Email")


def test_report_builder_supports_medical_agent_data():
    df = read_table(FIXTURES_DIR / "medical_agent_data.csv")

    group_report = build_group_report(df, group_column="代理人", value_column="項目金額")
    monthly_report = build_monthly_report(df, date_column="手術日期", value_column="金額")

    assert group_report.to_dict("records") == [
        {"代理人": "王代理", "筆數": 2, "項目金額總和": 27000, "項目金額平均值": 13500},
        {"代理人": "李代理", "筆數": 1, "項目金額總和": 18000, "項目金額平均值": 18000},
    ]
    assert monthly_report.to_dict("records") == [
        {"月份": "2026-01", "筆數": 2, "金額總和": 13000, "金額平均值": 6500},
        {"月份": "2026-02", "筆數": 1, "金額總和": 7000, "金額平均值": 7000},
    ]


def test_build_top10_report_limits_to_ten_rows():
    df = pd.DataFrame(
        {
            "項目": [f"項目{i}" for i in range(12)],
            "金額": list(range(12)),
        }
    )

    report = build_top10_report(df, value_column="金額")

    assert len(report) == 10
    assert report.iloc[0]["金額"] == 11
    assert report.iloc[-1]["金額"] == 2


def test_build_monthly_report_returns_empty_when_date_column_is_blank():
    df = pd.DataFrame({"日期": [None, None], "金額": [100, 200]})

    report = build_monthly_report(df, date_column="日期", value_column="金額")

    assert report.empty
    assert report.columns.tolist() == ["月份", "筆數", "金額總和", "金額平均值"]


def test_report_builder_validates_missing_columns():
    df = read_table(FIXTURES_DIR / "sales_data.csv")

    with pytest.raises(ValueError, match="找不到欄位"):
        build_group_report(df, group_column="不存在", value_column="金額")

    with pytest.raises(ValueError, match="找不到欄位"):
        build_summary(df, value_column="不存在")
