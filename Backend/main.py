from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "a24ff933811047d994b9e76f1e9d7280"
PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF", "NZD/USD"]

def fetch_candle(pair):
    symbol = pair.replace("/", "")
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=30&apikey={API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        return data.get("values", [])
    except:
        return []

def analyze(candles):
    if not candles or len(candles) < 10:
        return None
    last = candles[0]
    close_price = float(last['close'])

    # Simulated RSI value (you can replace with real RSI logic later)
    rsi = 30 + (hash(last['close']) % 40)

    if rsi < 35:
        action = "Buy"
    elif rsi > 65:
        action = "Sell"
    else:
        return None

    strength = int(abs(rsi - 50) * 2)
    if strength < 70:
        return None

    return {
        "pair": pair,
        "action": action,
        "strength": strength,
        "trend": "Uptrend" if action == "Buy" else "Downtrend",
        "rsi": rsi,
        "buy_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route("/api/latest-signals")
def latest_signals():
    signals = []
    for pair in PAIRS:
        data = fetch_candle(pair)
        signal = analyze(data)
        if signal:
            signals.append(signal)
        if len(signals) >= 2:
            break
    return jsonify({"signals": signals})

if __name__ == "__main__":
    app.run()
