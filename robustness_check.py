import pandas as pd
from backtest import run_backtest_with_metrics
from strategies.momentum import momentum_strategy

# Paste best params from tuning
best_params = {
    "window": 15,
    "threshold": 0.01,
    "min_hold": 5,
    "vol_threshold": 0.02,
    "vol_window": 10
}

#tickers = ["AAPL", "GOOG", "NVDA", "LMT", "META", "MSFT"] #Company Tickers
tickers = ["SPY", "QQQ", "TLT", "GLD"]
results = []

for ticker in tickers:
    try:
        df, metrics = run_backtest_with_metrics(
            strategy=momentum_strategy,
            ticker=ticker,
            period="6mo",
            interval="1d",
            transaction_cost=0.0005,
            **best_params
        )
        metrics["Ticker"] = ticker
        results.append(metrics)
        print(f"{ticker}: Sharpe={metrics['Sharpe Ratio']:.2f}, Final Return={metrics['Final Return']:.2f}, Max DD={metrics['Max Drawdown']:.2%}")
    except Exception as e:
        print(f"Failed on {ticker}: {e}")

# Save and display summary
summary_df = pd.DataFrame(results)
summary_df = summary_df[["Ticker", "Sharpe Ratio", "Final Return", "Max Drawdown"]]
print("\n--- Robustness Check Summary ---")
print(summary_df)
summary_df.to_csv("robustness_summary.csv", index=False)