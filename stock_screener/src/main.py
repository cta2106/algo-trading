from stock_screener.src.screen import screen_sp500_tickers
from stock_screener.src.trend import is_downtrending

if __name__ == "__main__":
    THRESHOLD_IN_DAYS = 1
    END_DATE_STR = "2021-01-01"

    sp500_matched = screen_sp500_tickers(
        is_downtrending, threshold_in_days=THRESHOLD_IN_DAYS, end_date_str=END_DATE_STR
    )
    print(sp500_matched)
