import datetime as dt
from typing import Callable

import pandas as pd
import plotly
import plotly.express as px

from intraday_trading.src.constants import DATE_FMT
from intraday_trading.src.strategies import StrategyParams


def _daily_pnl(
    df_day: pd.DataFrame, strategy: Callable, params: StrategyParams
) -> float:
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
    df_pnl = pd.DataFrame(
        {"date": unique_dates, "pnl": [0] + pnl[1:]}
    )  # index first pnl value at 0, cumulative_pnl at 1
    df_pnl["cumulative_pnl"] = (df_pnl["pnl"] + 1).cumprod()
    return df_pnl


def plot_cumulative_pnl(
    df_pnl: pd.DataFrame, df_daily: pd.DataFrame, asset: str
) -> plotly.graph_objects.Figure:
    df_plot = pd.DataFrame(
        {
            "System PnL": df_pnl.cumulative_pnl.values,
            "Buy and Hold PnL": (df_daily["pnl"] + 1).cumprod().fillna(1).values,
        },
        index=df_daily.index,
    )
    fig = px.line(
        df_plot,
        title=f"{asset} Cumulative Returns for {df_daily.index[0].strftime('%B %d, %Y')} - {df_daily.index[-1].strftime('%B %d, %Y')}",
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Returns",
        legend_title="Strategy",
        font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
    )

    fig.show()
