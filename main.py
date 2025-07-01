from backtest import run_backtest_with_metrics
from strategies.momentum import momentum_strategy

if __name__ == "__main__":
    print("Running backtest with momentum strategy...")

    df, metrics = run_backtest_with_metrics(
        strategy=momentum_strategy,
        ticker="AAPL",
        period="6mo",
        interval="1d",
        window=10,
        threshold=0.02,
        min_hold=3,
        vol_threshold=None, #Disabled volatility filter for now
        vol_window=10,
        transaction_cost=0.0005,
    )

    print("\n--- Strategy Performance Metrics ---")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")

    print("\n--- Final Backtest Snapshot ---")
    print(df.tail(10))