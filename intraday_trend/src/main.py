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
ASSET = "GOOGL"


def main() -> None:
    df = download_data(ASSET)
    df_pnl = get_pnl(
        df,
        entry_condition=config.entry_condition,
        exit_condition=config.exit_condition,
        entry_time_in_minutes=config.entry_time_in_minutes,
    )
    df_pnl.to_csv(directories.pnl_data / PNL_FILENAME, index=False)

    plot_cumulative_pnl(df_pnl)

    sr = sharpe_ratio(df_pnl)
    logger.info(f"Shape Ratio for this Strategy: {sr}")


if __name__ == "__main__":
    main()
