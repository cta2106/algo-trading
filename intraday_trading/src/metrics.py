import numpy as np
import pandas as pd


def sharpe_ratio(df_in: pd.DataFrame) -> float:
    return (252 ** 0.5) * np.mean(df_in["pnl"]) / np.std(df_in["pnl"])
