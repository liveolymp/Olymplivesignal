from flask import Flask, jsonify
import requests
from datetime import datetime

API_KEY = "a24ff933811047d994b9e76f1e9d7280"
pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]

app = Flask(__name__)

def fetch_data(pair):
    symbol = pair.replace("/", "")
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=30&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("values", [])

def analyze(candles):
    if not candles or len(candles) < 10:
        return None
    last = candles[0]
    rsi = 30 + (hash(last['close']) % 40)
    action = "Buy" if rsi < 35 else "Sell" if rsi > 65 else None
    if not action:
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
    for pair in pairs:
        data = fetch_data(pair)
        signal = analyze(data)
        if signal:
            signals.append(signal)
        if len(signals) >= 2:
            break
    return jsonify({"signals": signals})

if __name__ == "__main__":
    app.run()
