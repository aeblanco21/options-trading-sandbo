import pandas as pd

def momentum_strategy(data, window=5, threshold=0.02, min_hold=3, vol_window=5, vol_threshold=0.02):
    data = data.copy()

    # Momentum and volatility calculations
    data["Momentum"] = data["Close"] - data["Close"].shift(window)
    data["Volatility"] = data["Close"].pct_change().rolling(window=vol_window).std()

    signal = [0] * len(data)
    position = 0
    hold_days = 0

    for i in range(len(data)):
        if pd.isna(data["Momentum"].iloc[i]) or pd.isna(data["Volatility"].iloc[i]):
            continue

        momentum = data["Momentum"].iloc[i]
        vol = data["Volatility"].iloc[i]

        # --- Disable volatility filtering if vol_threshold is None ---
        vol_ok = vol_threshold is None or vol < vol_threshold

        if hold_days >= min_hold:
            if momentum > threshold and vol_ok:
                position = 1
                hold_days = 0
            elif momentum < -threshold and vol_ok:
                position = -1
                hold_days = 0
            else:
                position = 0
                hold_days = 0

        signal[i] = position
        hold_days += 1

    data["Signal"] = signal

    print("\n--- Strategy Debug Output ---")
    print(data[["Close", "Momentum", "Volatility", "Signal"]].dropna().tail(10))
    print("Signal counts:\n", data["Signal"].value_counts())

    return data["Signal"]