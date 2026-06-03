from ui import _value_column_options


def test_value_column_options_prefers_amount_columns_over_sequence_columns():
    options = _value_column_options(["序号", "金額", "日期序號", "項目金額"])

    assert options == ["金額", "項目金額", "序号", "日期序號"]
