import requests
from datetime import datetime
import json

TWELVE_DATA_API_KEY = "a24ff933811047d994b9e76f1e9d7280"
SYMBOLS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "NZD/USD",
    "USD/CAD", "EUR/GBP", "EUR/JPY", "GBP/JPY", "XAU/USD", "BTC/USD"
]

def fetch_data(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&apikey={TWELVE_DATA_API_KEY}&outputsize=2"
    response = requests.get(url)
    data = response.json()
    if "values" in data:
        return data["values"]
    else:
        print(f"⚠️ Failed to fetch: {symbol} -> {data}")
        return None

def calculate_rsi(closes):
    if len(closes) < 2:
        return 50
    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = float(closes[i]) - float(closes[i - 1])
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))
    avg_gain = sum(gains) / len(gains) if gains else 0.001
    avg_loss = sum(losses) / len(losses) if losses else 0.001
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_strength(rsi, volume_ok, trend_ok):
    strength = 0
    if 40 < rsi < 60:
        strength += 30
    if volume_ok:
        strength += 35
    if trend_ok:
        strength += 35
    return strength

def generate_latest_signals():
    signals = []
    for symbol in SYMBOLS:
        data = fetch_data(symbol)
        if not data or len(data) < 2:
            continue

        latest, prev = data[0], data[1]
        close_prices = [entry["close"] for entry in data]
        rsi = calculate_rsi(close_prices)

        volume_ok = float(latest["volume"]) > float(prev["volume"])
        trend_ok = float(latest["close"]) > float(latest["open"])
        strength = calculate_strength(rsi, volume_ok, trend_ok)

        # 🔍 Debug logs
        print(f"🟡 {symbol}: RSI={rsi:.2f}, VolOK={volume_ok}, TrendOK={trend_ok}, Strength={strength}")

        # 🧪 Filter is now off — allow all
        signal = {
            "pair": symbol,
            "action": "Buy" if trend_ok else "Sell",
            "rsi": round(rsi, 2),
            "strength": strength,
            "buy_time": datetime.utcnow().strftime("%H:%M UTC"),
            "timestamp": datetime.utcnow().isoformat()
        }
        signals.append(signal)

    # Save to history
    with open("signal_history.json", "w") as f:
        json.dump(signals, f)

    return signals
