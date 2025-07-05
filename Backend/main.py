from flask import Flask, jsonify
import requests
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)

API_KEY = "a24ff933811047d994b9e76f1e9d7280"
PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF", "NZD/USD"]

def fetch_candles(pair):
    symbol = pair.replace("/", "")
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=50&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("values", [])
    except:
        return []

def calculate_rsi(closes, period=14):
    deltas = np.diff(closes)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def analyze(pair):
    candles = fetch_candles(pair)
    if not candles or len(candles) < 20:
        return None

    df = pd.DataFrame(candles)
    df = df.astype({'close': 'float', 'volume': 'float'})
    closes = df['close'].tolist()
    volumes = df['volume'].tolist()
    rsi = calculate_rsi(closes)

    action = None
    if rsi < 45:
        action = "Buy"
    elif rsi > 55:
        action = "Sell"

    if not action:
        return None

    avg_volume = np.mean(volumes[-15:])
    last_volume = volumes[0]

    if last_volume < avg_volume * 0.95:
        return None

    strength = int(min(100, abs(rsi - 50) * 2))
    if strength < 40:
        return None

    return {
        "pair": pair,
        "action": action,
        "strength": strength,
        "rsi": rsi,
        "volume": last_volume,
        "trend": "Uptrend" if action == "Buy" else "Downtrend",
        "buy_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route("/api/latest-signals")
def latest_signals():
    results = []
    for pair in PAIRS:
        signal = analyze(pair)
        if signal:
            results.append(signal)
        if len(results) >= 2:
            break
    return jsonify({"signals": results})

@app.route("/")
def home():
    return "✅ Olymp Signal Backend (40%+ Strength Test Mode)"

if __name__ == "__main__":
    app.run()
