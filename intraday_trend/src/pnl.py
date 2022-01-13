import datetime as dt

import matplotlib
import pandas as pd
from matplotlib import pyplot as plt

from intraday_trend.src.constants import DATE_FMT


def _daily_pnl(
    df_day: pd.DataFrame,
    entry_condition: float,
    exit_condition: float,
    entry_time_in_minutes: int,
) -> float:
    return_at_entry = (
        df_day.iloc[entry_time_in_minutes]["open"] / df_day.iloc[0]["open"] - 1
    )
    tick_returns = df_day["open"].pct_change()
    pnl = 0.0
    if return_at_entry > entry_condition:
        buy_price = df_day.iloc[entry_time_in_minutes + 1]["open"]
        buy_time = df_day.iloc[entry_time_in_minutes + 1].name
        cumulated_returns = (tick_returns.loc[buy_time:] + 1).cumprod()
        exit_time = cumulated_returns[
            abs(cumulated_returns) > exit_condition
        ].first_valid_index()
        if exit_time is None:
            exit_price = df_day.iloc[-1]["open"]
        else:
            exit_price = df_day.loc[exit_time + dt.timedelta(minutes=1)]["open"]
        spread = exit_price - buy_price
        pnl = spread / buy_price
    return pnl


def get_pnl(
    df: pd.DataFrame,
    entry_condition: float,
    exit_condition: float,
    entry_time_in_minutes: int,
) -> pd.DataFrame:
    pnl = list()
    unique_dates = df.index.map(lambda t: t.date()).unique()
    for date in unique_dates:
        date_str = dt.datetime.strftime(date, DATE_FMT)
        df_day = df.loc[date_str]
        daily_pnl = _daily_pnl(
            df_day, entry_condition, exit_condition, entry_time_in_minutes
        )
        pnl.append(daily_pnl)
    return pd.DataFrame({"date": unique_dates, "pnl": pnl})


def plot_cumulative_pnl(
    df_pnl: pd.DataFrame, df: pd.DataFrame
) -> matplotlib.pyplot.figure:
    df_pnl["cumulative_pnl"] = (df_pnl["pnl"] + 1).cumprod()
    plt.plot(df_pnl.date, df_pnl.cumulative_pnl, color="red", label="System PnL")
    plt.plot(df.index, df.pnl + 1, color="blue", label="Buy and Hold PnL")

    plt.legend(loc="upper left")
    plt.show()
