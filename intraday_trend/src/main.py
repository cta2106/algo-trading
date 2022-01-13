import logging

from intraday_trend.src.config.config import get_config
from intraday_trend.src.config.directories import directories
from intraday_trend.src.constants import PNL_FILENAME
from intraday_trend.src.etl import download_data
from intraday_trend.src.metrics import sharpe_ratio
from intraday_trend.src.pnl import get_pnl, plot_cumulative_pnl

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


config = get_config()
ASSET = "SPY"


def main() -> None:
    df = download_data(ASSET)
    df["pnl"] = df.open.pct_change()

    df_pnl = get_pnl(
        df,
        entry_condition=config.entry_condition,
        exit_condition=config.exit_condition,
        entry_time_in_minutes=config.entry_time_in_minutes,
    )

    df_pnl.to_csv(directories.pnl_data / PNL_FILENAME, index=False)

    plot_cumulative_pnl(df_pnl, df)

    sr_s = sharpe_ratio(df_pnl)
    sr_bh = sharpe_ratio(df)

    logger.info(f"System Shape Ratio: {sr_s} \n Buy and Hold Sharpe Ratio: {sr_bh}")


if __name__ == "__main__":
    main()
