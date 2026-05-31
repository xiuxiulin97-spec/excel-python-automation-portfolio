from __future__ import annotations

import re

import pandas as pd


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(str(email).strip()))


def build_issue_report(df: pd.DataFrame) -> pd.DataFrame:
    issue_rows: list[dict[str, object]] = []

    for index, row in df.iterrows():
        name = str(row.get("姓名", "")).strip()
        phone = str(row.get("電話", "")).strip()
        email = str(row.get("Email", "")).strip()

        problems: list[str] = []
        if not name:
            problems.append("缺少姓名")
        if not phone and not email:
            problems.append("缺少電話或Email")
        if email and not is_valid_email(email):
            problems.append("Email格式錯誤")

        for problem in problems:
            issue_row = row.to_dict()
            issue_row["問題"] = problem
            issue_row["_source_index"] = index
            issue_rows.append(issue_row)

    if not issue_rows:
        return pd.DataFrame(columns=[*df.columns.tolist(), "問題", "_source_index"])

    return pd.DataFrame(issue_rows)
