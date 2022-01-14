import logging

from intraday_trend.src.config.config import get_config
from intraday_trend.src.config.directories import directories
from intraday_trend.src.constants import PNL_FILENAME
from intraday_trend.src.etl import download_data
from intraday_trend.src.metrics import sharpe_ratio
from intraday_trend.src.pnl import get_pnl, plot_cumulative_pnl
from intraday_trend.src.strategies import (
    TrendFollowingParams,
    trend_following,
    buy_late_sell_early,
    BuyLateSellEarlyParams,
)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = get_config()
ASSET = "PTON"

STRATEGY_FACTORY = {
    "trend_following": (trend_following, TrendFollowingParams),
    "buy_late_sell_early": (buy_late_sell_early, BuyLateSellEarlyParams),
}


def main(strategy) -> None:
    df = download_data(ASSET)
    df["pnl"] = df.open.pct_change()

    strategy, params = STRATEGY_FACTORY.get(strategy)
    params_dict = config.params.get(strategy.__name__)
    strategy_params = params(**params_dict) if params_dict else None

    df_pnl = get_pnl(
        df,
        strategy,
        strategy_params,
    )
    df_pnl.to_csv(directories.pnl_data / PNL_FILENAME, index=False)

    plot_cumulative_pnl(df_pnl, df, asset=ASSET)

    sr_s = sharpe_ratio(df_pnl)
    sr_bh = sharpe_ratio(df)

    logger.info(f"System Shape Ratio: {sr_s} \n Buy and Hold Sharpe Ratio: {sr_bh}")


if __name__ == "__main__":
    main("buy_late_sell_early")
