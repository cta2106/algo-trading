import datetime as dt
from typing import Callable, Dict

import pandas as pd
import plotly.graph_objects as go
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
    df_pnl: pd.DataFrame,
    df_daily: pd.DataFrame,
    asset: str,
    metrics: Dict[str, float],
    strategy_name: str,
) -> None:
    Y_ANNOTATION = 0.7
    Y_PAD = 0.06  # distance between metrics
    X_ANNOTATION = 1.02
    TOP_PADDING = 150
    RIGHT_PADDING = 430
    TITLE_TO_METRIC_PADDING = 1.35

    df_plot = pd.DataFrame(
        {
            "Buy and Hold PnL": (df_daily["pnl"] + 1).cumprod().fillna(1).values,
            f"{strategy_name.replace('_', ' ').title()} PnL": df_pnl.cumulative_pnl.values,
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
        margin=dict(t=TOP_PADDING, r=RIGHT_PADDING),
    )

    fig.add_annotation(
        go.layout.Annotation(
            text="Metrics",
            align="center",
            showarrow=False,
            xref="paper",
            xanchor="left",
            yref="paper",
            x=X_ANNOTATION,
            y=Y_ANNOTATION + Y_PAD / TITLE_TO_METRIC_PADDING,
            font=dict(family="Courier New, monospace", size=22, color="RebeccaPurple"),
        )
    )

    y_annotation = Y_ANNOTATION
    for metric_name, metric_value in metrics.items():
        fig.add_annotation(
            go.layout.Annotation(
                text="\n".join([f"{metric_name}: {metric_value:.2f}"]),
                align="center",
                showarrow=False,
                xref="paper",
                xanchor="left",
                yref="paper",
                x=X_ANNOTATION,
                y=y_annotation,
            )
        )
        y_annotation -= Y_PAD

    fig.show()
