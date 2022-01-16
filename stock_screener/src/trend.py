import datetime as dt

from stock_screener.src.etl import download_data


def is_downtrending(ticker: str, threshold_in_days: int, end_date_str: str) -> bool:
    start_date_str = (
        dt.datetime.strptime(end_date_str, "%Y-%m-%d")
        - dt.timedelta(days=threshold_in_days + 1)
    ).strftime("%Y-%m-%d")
    df_asset = download_data(
        ticker, start_date_str=start_date_str, end_date_str=end_date_str
    )
    df_asset["Returns"] = df_asset["Adj Close"].pct_change().shift(-1)
    return (df_asset["Returns"].values <= 0).all()
