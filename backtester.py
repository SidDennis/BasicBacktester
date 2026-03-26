import sys
import yfinance as yf
import pandas as pd 

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

if len(sys.argv) != 3:
  print("Usage: python3 backtester.py <TICKER> <PERIOD>")

ticker = sys.argv[1]
period = sys.argv[2]
tickerObject = yf.Ticker(ticker)
df = tickerObject.history(period=period)

df = df[['Close']]

# strategy
df['LastMean'] = df['Close'].rolling(5).mean().shift(1)
df['Buy'] = df["Close"] > df['LastMean']
df['Position'] = df['Buy'].fillna(False).astype(int)
# strategy

df['Return'] = df['Close'].pct_change()
df['Strategy_Return'] = df['Return'] * df['Position']

df[['Cumulative_Return', 'Cumulative_Strategy_Return']] = (1 + df[['Return', 'Strategy_Return']]).cumprod()

df[['Cumulative_Return', 'Cumulative_Strategy_Return']].plot(
    title='bullshit buy strategy',
    figsize=(10, 6)
)
plt.ylabel("Cumulative Return")
plt.show()



