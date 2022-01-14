import datetime as dt
import logging
import os
from typing import Dict

import pandas as pd
from tiingo import TiingoClient

from intraday_trend.src.config.config import get_config
from intraday_trend.src.config.directories import directories
from intraday_trend.src.constants import DATE_FMT
from intraday_trend.src.utils import get_date_slices

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = get_config()


def download_data(asset: str) -> pd.DataFrame:
    tiingo_config = {
        "api_key": os.getenv("TIINGO_API_KEY"),
        "session": True,  # Reuse HTTP sessions across API calls for better performance
    }

    df = _get_intraday_minute_data(
        asset,
        start_date_str=config.start_date_str,
        end_date_str=config.end_date_str,
        tiingo_config=tiingo_config,
    )
    df.to_csv(directories.price_data / f"{asset.lower()}.csv", index=False)
    logger.info(f"{asset.lower()}.csv generated!")
    return df


def _get_intraday_minute_data(
    ticker: str, *, start_date_str: str, end_date_str: str, tiingo_config: Dict
) -> pd.DataFrame:
    client = TiingoClient(tiingo_config)
    date_slices = get_date_slices(start_date_str, end_date_str)
    json_data = list()
    for idx, (start_date_str, end_date_str) in enumerate(date_slices):
        if idx != 0:
            start_date_str = dt.datetime.strptime(
                start_date_str, DATE_FMT
            ) + dt.timedelta(days=1)
        json_data.extend(
            client.get_ticker_price(
                ticker,
                fmt="json",
                startDate=start_date_str,
                endDate=end_date_str,
                frequency="1MIN",
            )
        )
    data = pd.json_normalize(json_data)

    data["date"] = pd.to_datetime(data["date"]).dt.tz_convert("America/New_York")
    return data.set_index("date")
