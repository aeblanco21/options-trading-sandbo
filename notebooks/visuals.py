def plot_backtest(df):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label="Close Price")

    equity = df["Cumulative Return"] * df["Close"].iloc[0]
    plt.plot(df.index, equity, label="Strategy Equity Curve")

    buy_signals = df[df["Signal"] == 1]
    sell_signals = df[df["Signal"] == -1]
    plt.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="green", label="Buy", alpha=0.6)
    plt.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red", label="Sell", alpha=0.6)

    plt.title("Momentum Strategy Backtest with Buy/Sell Signals")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()