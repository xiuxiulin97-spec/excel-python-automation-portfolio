import pandas as pd

from validator import build_issue_report, is_valid_email


def test_is_valid_email_accepts_common_email_format():
    assert is_valid_email("user@example.com")
    assert is_valid_email("user.name+tag@example.co")


def test_is_valid_email_rejects_invalid_email_format():
    assert not is_valid_email("not-email")
    assert not is_valid_email("user@")
    assert not is_valid_email("@example.com")


def test_build_issue_report_marks_invalid_email_missing_name_and_missing_contact():
    df = pd.DataFrame(
        [
            {"姓名": "王小明", "電話": "0912345678", "Email": "bad-email", "公司": "A公司"},
            {"姓名": "", "電話": "0912345678", "Email": "ok@example.com", "公司": "B公司"},
            {"姓名": "陳美華", "電話": "", "Email": "", "公司": "C公司"},
        ]
    )

    issues = build_issue_report(df)

    assert issues["問題"].tolist() == [
        "Email格式錯誤",
        "缺少姓名",
        "缺少電話或Email",
    ]
