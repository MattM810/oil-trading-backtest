# WTI Oil Monthly Momentum Backtest

A Python backtesting model analysing a momentum strategy on WTI crude oil futures using 14 years of monthly price data (2010–2024).

## Strategy
- Buy signal: price is above its 3-month moving average AND previous month's return is positive
- Sell signal: either condition breaks — move to cash
- Rebalanced monthly

## Results
| Strategy | Return |
|---|---|
| Momentum | +214.1% |
| Buy & Hold WTI | -12.1% |

- 180 monthly data points
- 34 trade signals
- 47% time in market

## Key Finding
The momentum filter avoided the 2015 oil crash (-60%) and the 2020 COVID crash, which destroyed buy and hold returns over the period.

## Libraries
Python, pandas, numpy, matplotlib
