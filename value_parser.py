from __future__ import annotations

import re
from typing import Any

import pandas as pd


_CURRENCY_PATTERN = re.compile(r"(nt\$|rmb|cny|usd|twd|[$￥¥元圓圆])", re.IGNORECASE)
_NUMBER_PATTERN = re.compile(r"^-?\d+(?:\.\d+)?$")


def parse_amount(value: Any) -> float | None:
    """Parse common ledger amount formats.

    Returns None for blank values or text that is not a clean amount.
    """
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    negative = text.startswith("(") and text.endswith(")")
    if negative:
        text = text[1:-1].strip()

    text = text.replace(",", "").replace("，", "").replace(" ", "")
    text = _CURRENCY_PATTERN.sub("", text)

    if not _NUMBER_PATTERN.match(text):
        return None

    amount = float(text)
    return -amount if negative else amount


def parse_amount_series(series: pd.Series) -> pd.Series:
    return series.map(parse_amount)
