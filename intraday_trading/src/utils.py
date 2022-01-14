import datetime as dt
from typing import List, Tuple

import pandas as pd

from intraday_trend.src.constants import (
    DATE_FMT,
    TIINGO_ROW_LIMIT,
    MINUTES_PER_TRADING_DAY,
)


def get_sp500_tickers(url: str) -> List[str]:
    tables = pd.read_html(url)
    sp500_tickers = tables[0]["Symbol"].tolist()
    return sp500_tickers


def get_date_slices(start_date_str: str, end_date_str: str) -> List[Tuple[str, str]]:
    """Return chunks between start_date and end_date to allow chaining of API calls so that limit is not hit."""
    start_date = dt.datetime.strptime(start_date_str, DATE_FMT)
    end_date = dt.datetime.strptime(end_date_str, DATE_FMT)

    dates = pd.date_range(
        start_date, end_date, freq=f"{TIINGO_ROW_LIMIT // MINUTES_PER_TRADING_DAY}d"
    ).tolist()
    if end_date not in dates:
        dates.append(end_date)
    dates_str = [dt.datetime.strftime(date, DATE_FMT) for date in dates]
    return list(zip(dates_str, dates_str[1:]))
