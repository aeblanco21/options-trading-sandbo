import pandas as pd
import numpy as np

def mean_reversion_strategy(data, window=20, num_std=1.5, min_hold=3, vol_threshold=None, vol_window=10):
    """
    Mean Reversion Strategy using Bollinger Bands and optional volatility filter.

    Parameters:
        data (pd.DataFrame): Must contain a 'Close' price column.
        window (int): Lookback window for moving average.
        num_std (float): Number of standard deviations for bands.
        min_hold (int): Minimum number of days to hold a position.
        vol_threshold (float or None): If set, filters signals by rolling volatility.
        vol_window (int): Lookback window for volatility.

    Returns:
        pd.Series: Signal series (-1 for short, 1 for long, 0 for neutral).
    """
    df = data.copy()
    df["SMA"] = df["Close"].rolling(window=window).mean()
    df["STD"] = df["Close"].rolling(window=window).std()
    df["Lower Band"] = df["SMA"] - num_std * df["STD"]
    df["Upper Band"] = df["SMA"] + num_std * df["STD"]

    signal = np.zeros(len(df))

    for i in range(1, len(df)):
        # Long signal: price crosses below lower band
        if df["Close"].iloc[i - 1] > df["Lower Band"].iloc[i - 1] and df["Close"].iloc[i] < df["Lower Band"].iloc[i]:
            signal[i] = 1
        # Short signal: price crosses above upper band
        elif df["Close"].iloc[i - 1] < df["Upper Band"].iloc[i - 1] and df["Close"].iloc[i] > df["Upper Band"].iloc[i]:
            signal[i] = -1

    # Apply volatility filter (optional)
    if vol_threshold is not None:
        df["Volatility"] = df["Close"].pct_change().rolling(vol_window).std()
        signal = np.where(df["Volatility"] > vol_threshold, 0, signal)

    # Enforce min_hold constraint
    for i in range(1, len(signal)):
        if signal[i] == 0 and signal[i - 1] != 0:
            for j in range(1, min_hold):
                if i + j < len(signal) and signal[i + j] == 0:
                    signal[i + j] = signal[i - 1]

    return pd.Series(signal, index=df.index)