import datetime as dt
from abc import abstractmethod
from dataclasses import dataclass

import pandas as pd


@abstractmethod
@dataclass
class StrategyParams:
    pass


@dataclass
class TrendFollowingParams(StrategyParams):
    entry_time_in_minutes: int
    entry_condition: float
    exit_condition: float


@dataclass()
class BuyLateSellEarlyParams(StrategyParams):
    pass


def trend_following(df_day: pd.DataFrame, params: TrendFollowingParams) -> float:
    return_at_entry = (
        df_day.iloc[params.entry_time_in_minutes]["open"] / df_day.iloc[0]["open"] - 1
    )
    tick_returns = df_day["open"].pct_change()
    pnl = 0.0
    if return_at_entry > params.entry_condition:
        buy_price = df_day.iloc[params.entry_time_in_minutes + 1]["open"]
        buy_time = df_day.iloc[params.entry_time_in_minutes + 1].name
        cumulated_returns = (tick_returns.loc[buy_time:] + 1).cumprod()
        exit_time = cumulated_returns[
            abs(cumulated_returns) > params.exit_condition
        ].first_valid_index()
        if exit_time is None:
            exit_price = df_day.iloc[-1]["open"]
        else:
            exit_price = df_day.loc[exit_time + dt.timedelta(minutes=1)]["open"]
        spread = exit_price - buy_price
        pnl = spread / buy_price
    return pnl


def buy_late_sell_early(df_day: pd.DataFrame, params: BuyLateSellEarlyParams) -> float:
    exit_price = df_day.iloc[0]["open"]
    buy_price = df_day.iloc[-1]["close"]
    spread = exit_price - buy_price
    return spread / buy_price
