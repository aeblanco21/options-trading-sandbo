import yfinance as yf
import pandas as pd
import numpy as np

def run_backtest(strategy, ticker="AAPL", period="6mo", interval="1d",
                 window=5, threshold=0.02, min_hold=3,
                 vol_threshold=0.02, vol_window=5, transaction_cost=0.001):
    # Download historical price data
    data = yf.download(ticker, period=period, interval=interval, group_by="ticker", auto_adjust=True)

    # Drop unnecessary multi-index if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(0)

    data = data.reset_index()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.dropna(subset=["Date"])
    data = data.set_index("Date")

    if "Close" not in data.columns:
        raise ValueError(f"'Close' column not found. Columns: {list(data.columns)}")

    # Generate strategy signals
    data["Signal"] = strategy(
        data.copy(),
        window=window,
        threshold=threshold,
        min_hold=min_hold,
        vol_threshold=vol_threshold,
        vol_window=vol_window
    )

    # Daily returns
    data["Daily Return"] = data["Close"].pct_change()
    data["Strategy Return"] = data["Signal"].shift(1) * data["Daily Return"]

    # Transaction costs
    trades = data["Signal"].shift(1).diff().abs().fillna(0)
    data["Transaction Cost"] = trades * transaction_cost
    data["Net Strategy Return"] = data["Strategy Return"] - data["Transaction Cost"]

    # Cumulative performance
    data["Cumulative Return"] = (1 + data["Net Strategy Return"]).cumprod()

    # Debug info
    print("\n--- Strategy Debug Output ---")
    print(data[["Close", "Signal"]].tail(10))

    return data[["Close", "Signal", "Net Strategy Return", "Cumulative Return"]]



def run_backtest_with_metrics(strategy, ticker="AAPL", period="6mo", interval="1d",
                              window=5, threshold=0.02, min_hold=3,
                              vol_threshold=0.02, vol_window=5, transaction_cost=0.001):
    """
    Wraps run_backtest and calculates:
    - Sharpe Ratio
    - Max Drawdown
    - Final Return
    """
    df = run_backtest(
        strategy=strategy,
        ticker=ticker,
        period=period,
        interval=interval,
        window=window,
        threshold=threshold,
        min_hold=min_hold,
        vol_threshold=vol_threshold,
        vol_window=vol_window,
        transaction_cost=transaction_cost
    )

    returns = df["Net Strategy Return"].dropna()
    cumulative = df["Cumulative Return"].dropna()

    sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else np.nan
    max_dd = (cumulative / cumulative.cummax() - 1).min()
    final_return = cumulative.iloc[-1] if not cumulative.empty else np.nan

    metrics = {
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd,
        "Final Return": final_return
    }

    return df, metrics

    total_trades = trades.sum()
    print(f"Total trades executed: {total_trades}")
    print(f"Average holding period: {len(data) / (total_trades if total_trades else 1):.2f} days")