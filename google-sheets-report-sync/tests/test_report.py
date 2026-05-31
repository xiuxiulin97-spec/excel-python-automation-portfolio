import pandas as pd
import pytest

from report import build_summary, validate_required_columns


def test_build_summary_groups_amount_by_customer():
    df = pd.DataFrame(
        {
            "客戶": ["A公司", "A公司", "B公司"],
            "金額": [1000, 3000, 2000],
        }
    )

    summary_df = build_summary(df)

    assert summary_df.to_dict("records") == [
        {"客戶": "A公司", "金額總和": 4000},
        {"客戶": "B公司", "金額總和": 2000},
    ]


def test_validate_required_columns_raises_when_customer_is_missing():
    df = pd.DataFrame({"金額": [1000]})

    with pytest.raises(ValueError, match="缺少必要欄位：客戶"):
        validate_required_columns(df)


def test_validate_required_columns_raises_when_amount_is_missing():
    df = pd.DataFrame({"客戶": ["A公司"]})

    with pytest.raises(ValueError, match="缺少必要欄位：金額"):
        validate_required_columns(df)


def test_build_summary_raises_when_amount_is_not_numeric():
    df = pd.DataFrame({"客戶": ["A公司"], "金額": ["abc"]})

    with pytest.raises(ValueError, match="金額欄位包含無法轉換成數字的資料"):
        build_summary(df)
