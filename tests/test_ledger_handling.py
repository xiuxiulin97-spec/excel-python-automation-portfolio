import pandas as pd

from column_analyzer import analyze_columns
from report_builder import (
    build_group_report,
    build_monthly_report,
    build_summary,
    build_top10_report,
)


def test_ledger_amount_blank_values_are_ignored_in_reports():
    df = pd.DataFrame(
        [
            {"用途": "食材", "金額": 37.49, "日期": 45686},
            {"用途": "調味品", "金額": None, "日期": 45687},
            {"用途": "食材", "金額": 24.6, "日期": 45688},
        ]
    )

    summary = build_summary(df, value_column="金額")
    group_report = build_group_report(df, group_column="用途", value_column="金額")
    top10_report = build_top10_report(df, value_column="金額")
    monthly_report = build_monthly_report(df, date_column="日期", value_column="金額")

    assert summary.to_dict("records") == [
        {"項目": "總筆數", "值": 3},
        {"項目": "金額總和", "值": 62.09},
        {"項目": "金額平均值", "值": 31.045},
    ]
    assert group_report.to_dict("records") == [
        {"用途": "食材", "筆數": 2, "金額總和": 62.09, "金額平均值": 31.045}
    ]
    assert top10_report["金額"].tolist() == [37.49, 24.6]
    assert monthly_report["筆數"].sum() == 2
    assert monthly_report["金額總和"].sum() == 62.09


def test_ledger_excel_serial_date_column_is_detected_as_date():
    df = pd.DataFrame(
        {
            "序号": [1, 2, 3],
            "日期": [45686, 45687, 45688],
            "用途": ["食材", "調味品", "食材"],
            "金額": [37.49, 24.6, 79],
        }
    )

    result = {item["name"]: item["type"] for item in analyze_columns(df)}

    assert result["序号"] == "number"
    assert result["日期"] == "date"
    assert result["用途"] == "text"
    assert result["金額"] == "number"


def test_ledger_amount_text_formats_can_be_summarized():
    df = pd.DataFrame(
        [
            {"用途": "食材", "金額": "37.49元"},
            {"用途": "食材", "金額": "￥1,200.50"},
            {"用途": "調味品", "金額": "NT$ 300"},
            {"用途": "退款", "金額": "(100)"},
            {"用途": "備註", "金額": "雞雜10斤"},
        ]
    )

    summary = build_summary(df, value_column="金額")
    group_report = build_group_report(df, group_column="用途", value_column="金額")
    top10_report = build_top10_report(df, value_column="金額")

    assert summary.to_dict("records") == [
        {"項目": "總筆數", "值": 5},
        {"項目": "金額總和", "值": 1437.99},
        {"項目": "金額平均值", "值": 359.4975},
    ]
    assert group_report.to_dict("records") == [
        {"用途": "食材", "筆數": 2, "金額總和": 1237.99, "金額平均值": 618.995},
        {"用途": "調味品", "筆數": 1, "金額總和": 300, "金額平均值": 300},
        {"用途": "退款", "筆數": 1, "金額總和": -100, "金額平均值": -100},
    ]
    assert top10_report["金額"].tolist() == [1200.5, 300, 37.49, -100]


def test_ledger_amount_text_formats_are_detected_as_number():
    df = pd.DataFrame(
        {
            "用途": ["食材", "食材", "調味品", "退款"],
            "金額": ["37.49元", "￥1,200.50", "NT$ 300", "(100)"],
        }
    )

    result = {item["name"]: item["type"] for item in analyze_columns(df)}

    assert result["用途"] == "text"
    assert result["金額"] == "number"
