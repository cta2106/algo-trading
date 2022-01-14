import datetime as dt
from typing import Callable

import matplotlib
import pandas as pd
from matplotlib import pyplot as plt

from intraday_trading.src.constants import DATE_FMT
from intraday_trading.src.strategies import StrategyParams


def _daily_pnl(
    df_day: pd.DataFrame, strategy: Callable, params: StrategyParams
) -> pd.DataFrame:
    pnl = strategy(df_day, params)
    return pnl


def get_pnl(
    df: pd.DataFrame, strategy: Callable, params: StrategyParams
) -> pd.DataFrame:
    pnl = list()
    unique_dates = df.index.map(lambda t: t.date()).unique()
    for date in unique_dates:
        date_str = dt.datetime.strftime(date, DATE_FMT)
        df_day = df.loc[date_str]
        daily_pnl = _daily_pnl(df_day, strategy, params)
        pnl.append(daily_pnl)
    return pd.DataFrame({"date": unique_dates, "pnl": pnl})


def plot_cumulative_pnl(
    df_pnl: pd.DataFrame, df: pd.DataFrame, asset: str
) -> matplotlib.pyplot.figure:
    df_pnl["cumulative_pnl"] = (df_pnl["pnl"] + 1).cumprod()
    plt.title(f"{asset} Cumulative Returns")
    plt.plot(df_pnl.date, df_pnl.cumulative_pnl, color="red", label="System PnL")
    plt.plot(
        df.index, (df["pnl"] + 1).cumprod(), color="blue", label="Buy and Hold PnL"
    )

    plt.legend(loc="upper left")
    plt.show()
