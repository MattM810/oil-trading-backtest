"""
WTI Oil Monthly Momentum Backtest (2010-2024)
----------------------------------------------
Strategy:
- Import monthly WTI crude oil prices from CSV
- Buy signal: price is above its 3-month moving average AND previous month's return is positive
- Sell signal: either condition breaks — move to cash
- Rebalanced monthly

Data source: wti_monthly_prices.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# --- Load data from CSV ---
df = pd.read_csv("wti_monthly_prices.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# --- Indicators ---
df["monthly_return"] = df["price"].pct_change() * 100
df["ma3"] = df["price"].rolling(3).mean()
df["ma12"] = df["price"].rolling(12).mean()

# --- Signals ---
df["signal"] = 0
for i in range(1, len(df)):
    price = df["price"].iloc[i]
    ma3 = df["ma3"].iloc[i]
    prev_return = df["monthly_return"].iloc[i]
    if pd.notna(ma3) and price > ma3 and prev_return > 0:
        df.iloc[i, df.columns.get_loc("signal")] = 1
    else:
        df.iloc[i, df.columns.get_loc("signal")] = 0

# --- Backtest ---
STARTING_CAPITAL = 10000
cap_momentum = STARTING_CAPITAL
cap_bh = STARTING_CAPITAL
cap_momentum_hist = []
cap_bh_hist = []

trades = 0
in_trade = False

for i in range(1, len(df)):
    ret = df["monthly_return"].iloc[i] / 100
    signal = df["signal"].iloc[i - 1]

    cap_bh = cap_bh * (1 + ret)

    if signal == 1:
        cap_momentum = cap_momentum * (1 + ret)
        if not in_trade:
            trades += 1
            in_trade = True
    else:
        in_trade = False

    cap_momentum_hist.append(cap_momentum)
    cap_bh_hist.append(cap_bh)

plot_dates = df.index[1:]
signals = df["signal"].iloc[1:]

momentum_return = (cap_momentum - STARTING_CAPITAL) / STARTING_CAPITAL * 100
bh_return = (cap_bh - STARTING_CAPITAL) / STARTING_CAPITAL * 100
months_in_market = signals.sum()
total_months = len(signals)

print("\n📊 WTI OIL MONTHLY MOMENTUM BACKTEST (2010–2024)")
print("=" * 55)
print(f"   Data points:          {len(df)} monthly prices")
print(f"   Time in market:       {int(months_in_market)}/{total_months} months ({months_in_market/total_months*100:.0f}%)")
print(f"   Trade signals:        {trades}")
print("=" * 55)
print(f"\n💰 $10,000 starting capital:")
print(f"   Momentum strategy:    ${cap_momentum:>8,.0f}  ({momentum_return:+.1f}%)")
print(f"   Buy & Hold WTI:       ${cap_bh:>8,.0f}  ({bh_return:+.1f}%)")
print(f"\n{'✅ Momentum WINS' if cap_momentum > cap_bh else '❌ Buy & Hold wins'}")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(13, 12))
fig.suptitle("WTI Oil Monthly Momentum Backtest (2010–2024)", fontsize=14, fontweight="bold")

ax1.plot(plot_dates, cap_momentum_hist, color="#2ecc71", linewidth=2,
         marker="o", markersize=5, label=f"Momentum ({momentum_return:+.1f}%)")
ax1.plot(plot_dates, cap_bh_hist, color="#3498db", linewidth=2,
         marker="o", markersize=5, label=f"Buy & Hold ({bh_return:+.1f}%)")
ax1.axhline(STARTING_CAPITAL, color="gray", linewidth=0.8, linestyle="--", label="$10k start")
ax1.set_ylabel("Portfolio Value ($)")
ax1.set_title("$10,000 Capital Growth")
ax1.legend()
ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))

ax2.plot(df.index, df["price"], color="#e74c3c", linewidth=1.5, label="WTI Price")
ax2.plot(df.index, df["ma3"], color="#f39c12", linewidth=1.2, linestyle="--", label="3-Month MA")
ax2.plot(df.index, df["ma12"], color="#8e44ad", linewidth=1.2, linestyle="--", label="12-Month MA")
ax2.fill_between(df.index, df["price"].min(), df["price"],
                 where=df["signal"] == 1, alpha=0.15, color="#2ecc71", label="In market")
ax2.set_ylabel("Price (USD/barrel)")
ax2.set_title("Oil Price with Moving Averages & Trade Signals")
ax2.legend()
ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))

colors = ["#2ecc71" if r > 0 else "#e74c3c" for r in df["monthly_return"].iloc[1:]]
ax3.bar(plot_dates, df["monthly_return"].iloc[1:], color=colors, width=20)
ax3.axhline(0, color="black", linewidth=0.8)
ax3.set_ylabel("Monthly Return (%)")
ax3.set_title("Monthly Returns (green = positive, red = negative)")
ax3.yaxis.set_major_formatter(mtick.PercentFormatter())

plt.tight_layout()
plt.savefig("oil_monthly_backtest.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n✅ Chart saved.")
