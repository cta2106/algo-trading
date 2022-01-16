from typing import List, Callable

import pandas as pd

from stock_screener.src.constants import SP500_URL


def _get_sp500_tickers() -> List[str]:
    df_sp500 = pd.read_html(SP500_URL)[0]
    return df_sp500["Symbol"].tolist()


def screen_sp500_tickers(checker: Callable, **kwargs) -> List[str]:
    asset_list = _get_sp500_tickers()
    sp500_matched = [asset for asset in asset_list if checker(asset, **kwargs)]
    return sp500_matched
