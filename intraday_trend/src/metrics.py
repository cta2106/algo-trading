import numpy as np
import pandas as pd


def sharpe_ratio(df_pnl: pd.DataFrame) -> float:
    return (252 ** 0.5) * np.mean(df_pnl["pnl"]) / np.std(df_pnl["pnl"])
