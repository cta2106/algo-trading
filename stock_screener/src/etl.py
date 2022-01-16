import pandas as pd
import yfinance as yf


def download_data(asset: str, start_date_str: str, end_date_str: str) -> pd.DataFrame:
    data = yf.download(asset, start=start_date_str, end=end_date_str, progress=False)
    data["Ticker"] = asset
    return data
