import logging

from intraday_trading.src.config.config import get_config
from intraday_trading.src.config.directories import directories
from intraday_trading.src.constants import PNL_FILENAME
from intraday_trading.src.etl import download_data
from intraday_trading.src.metrics import sharpe_ratio
from intraday_trading.src.pnl import get_pnl, plot_cumulative_pnl
from intraday_trading.src.strategies import (
    TrendFollowingParams,
    trend_following,
    buy_late_sell_early,
    BuyLateSellEarlyParams,
)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = get_config()

STRATEGY_FACTORY = {
    "trend_following": (trend_following, TrendFollowingParams),
    "buy_late_sell_early": (buy_late_sell_early, BuyLateSellEarlyParams),
}


def run_main(strategy_name: str, asset: str) -> None:
    df = download_data(asset)
    df_daily = df.resample("D").median().dropna()
    df_daily["pnl"] = df_daily["close"].pct_change()

    strategy, params = STRATEGY_FACTORY.get(strategy_name)
    params_dict = config.params.get(strategy.__name__)
    strategy_params = params(**params_dict) if params_dict else None

    df_pnl = get_pnl(
        df,
        strategy,
        strategy_params,
    )
    df_pnl.to_csv(directories.pnl_data / PNL_FILENAME, index=False)

    plot_cumulative_pnl(df_pnl, df_daily, asset=ASSET)
    logger.info(
        f"System Shape Ratio: {sharpe_ratio(df_pnl)} \n Buy and Hold Sharpe Ratio: {sharpe_ratio(df_daily)}"
    )


if __name__ == "__main__":
    ASSET = "BABA"
    STRATEGY_NAME = "buy_late_sell_early"

    run_main(STRATEGY_NAME, ASSET)
