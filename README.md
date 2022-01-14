# Intraday algorithmic trading

This repository enables the backtesting of two algorithmic trading strategies:

1. First, a momentum / trend-following intraday strategy that consists of:
   - Purchasing an asset 2 hours into the trading day if its price has increased by 2% or more from open
   - Exiting the trade if one of the following conditions is met:
     - The asset has gained 1% in value
     - The asset has lost 1% in value (stop-loss)
     - The trading day ended without any of the above conditions being met

  ![alt text](https://github.com/cta2106/algo-trading/blob/master/mrna_cumulative_returns.png)

  This strategy is inspired from Algovibes' video [here](https://www.youtube.com/watch?v=BhOdgrxWi5c).

2. Second, a simple buy late / sell early strategy, by which the algorithm enters a trade at close and exits it the next morning at open.

![alt text](https://github.com/cta2106/algo-trading/blob/master/pton_cumulative_returns.png)

## Data Source
Intraday financial data at the minute granularity can be acquired free of charge using the [Tiingo](https://www.tiingo.com/) API.
You will need a Tiingo API key to be able to run this code.

## Running Instructions
- Create a virtual environment
- Install projet requirements by running the command `pip install -r requirements.txt`
- Navigate to the `src` folder and run the following commands:
  - `export TIINGO_API_KEY = <YOUR_API_KEY>`
  - `python main.py`

You can set your asset ticker directly in `main.py` and if you so choose, modify the strategy parameters in `intraday_trend/config/config.yaml`.

## Disclaimer


NOT INVESTMENT ADVICE

This code is posted for informational purposes only. Nothing contained in this codebase constitutes a solicitation, recommendation, endorsement, or offer by the author to buy or sell any securities utilizing the algorithms implemented herewith.
