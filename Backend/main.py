import requests
from datetime import datetime, timedelta

API_KEY = "a24ff933811047d994b9e76f1e9d7280"
pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "NZD/USD", "USD/CHF", "EUR/JPY"]

def fetch_candle(pair):
    symbol = pair.replace("/", "")
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=50&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("values", [])

def calculate_signal(candles):
    if not candles or len(candles) < 10:
        return None

    last = candles[0]
    rsi = 30 + (hash(last['close']) % 40)  # Fake RSI for now (can use real formula)
    volume = float(last['volume'])

    # Signal Logic
    if rsi < 35:
        action = "Buy"
    elif rsi > 65:
        action = "Sell"
    else:
        return None

    # Simulate strength % based on RSI distance from neutral 50
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

def get_signals():
    signals = []
    for pair in pairs:
        candles = fetch_candle(pair)
        signal = calculate_signal(candles)
        if signal:
            signals.append(signal)
        if len(signals) >= 2:
            break
    return {"signals": signals}

# Flask server
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/api/latest-signals")
def latest_signals():
    return jsonify(get_signals())

if __name__ == "__main__":
    app.run(debug=True)
