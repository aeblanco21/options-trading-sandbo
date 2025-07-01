import itertools
import numpy as np
from backtest import run_backtest_with_metrics
from strategies.momentum import momentum_strategy

# Define the search space
param_grid = {
    "window": [5, 10, 15],
    "threshold": [0.01, 0.02, 0.03],
    "min_hold": [1, 3, 5],
    "vol_threshold": [None, 0.02, 0.015],
    "vol_window": [5, 10],
}

#tickers = ["AAPL", "GOOG", "NVDA", "LMT", "META", "MSFT"] #Company Tickers
tickers = ["SPY", "QQQ", "TLT", "GLD"]

# Create all combinations
all_combinations = list(itertools.product(
    param_grid["window"],
    param_grid["threshold"],
    param_grid["min_hold"],
    param_grid["vol_threshold"],
    param_grid["vol_window"],
))

results = []

print(f"Evaluating {len(all_combinations)} parameter combinations across {len(tickers)} tickers...\n")

for combo in all_combinations:
    window, threshold, min_hold, vol_threshold, vol_window = combo

    sharpe_values = []
    return_values = []

    for ticker in tickers:
        try:
            _, metrics = run_backtest_with_metrics(
                strategy=momentum_strategy,
                ticker=ticker,
                period="6mo",
                interval="1d",
                window=window,
                threshold=threshold,
                min_hold=min_hold,
                vol_threshold=vol_threshold,
                vol_window=vol_window,
                transaction_cost=0.0005,
            )
            sharpe_values.append(metrics["Sharpe Ratio"])
            return_values.append(metrics["Final Return"])

        except Exception as e:
            # Skip this configuration if one ticker fails
            sharpe_values = []
            break

    if sharpe_values:
        avg_sharpe = np.mean(sharpe_values)
        std_sharpe = np.std(sharpe_values)
        avg_return = np.mean(return_values)

        score = avg_sharpe - 0.5 * std_sharpe

        results.append({
            "window": window,
            "threshold": threshold,
            "min_hold": min_hold,
            "vol_threshold": vol_threshold,
            "vol_window": vol_window,
            "avg_sharpe": avg_sharpe,
            "std_sharpe": std_sharpe,
            "avg_final_return": avg_return,
            "score": score
        })

# Sort by robustness score (Sharpe penalized by volatility)
results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)

print("\n📈 Top 5 Robust Configurations:\n")
for r in results_sorted[:5]:
    print({
        "window": r["window"],
        "threshold": r["threshold"],
        "min_hold": r["min_hold"],
        "vol_threshold": r["vol_threshold"],
        "vol_window": r["vol_window"],
        "avg_sharpe": round(r["avg_sharpe"], 3),
        "std_sharpe": round(r["std_sharpe"], 3),
        "score": round(r["score"], 3),
        "avg_final_return": round(r["avg_final_return"], 3),
    })