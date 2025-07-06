import requests
from datetime import datetime, timedelta
import pytz
import json

API_KEY = "a24ff933811047d994b9e76f1e9d7280"
BASE_URL = "https://api.twelvedata.com"
IST = pytz.timezone("Asia/Kolkata")

# All major forex pairs from TwelveData
SYMBOLS = [
    "AUD/CAD", "AUD/CHF", "AUD/JPY", "AUD/NZD", "AUD/USD",
    "CAD/CHF", "CAD/JPY", "CHF/JPY", "EUR/AUD", "EUR/CAD",
    "EUR/CHF", "EUR/GBP", "EUR/JPY", "EUR/NZD", "EUR/USD",
    "GBP/AUD", "GBP/CAD", "GBP/CHF", "GBP/JPY", "GBP/NZD",
    "GBP/USD", "NZD/CAD", "NZD/CHF", "NZD/JPY", "NZD/USD",
    "USD/CAD", "USD/CHF", "USD/JPY", "USD/INR"
]

def get_ohlc(symbol, count=20):
    url = f"{BASE_URL}/time_series"
    params = {
        "symbol": symbol,
        "interval": "1min",
        "outputsize": count,
        "apikey": API_KEY,
        "timezone": "Asia/Kolkata"
    }
    try:
        response = requests.get(url, params=params)
        return response.json().get("values", [])
    except:
        return []

def calculate_rsi(candles, period=14):
    gains, losses = [], []
    for i in range(1, period + 1):
        diff = float(candles[i-1]["close"]) - float(candles[i]["close"])
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))
    if not gains or not losses:
        return 50
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def detect_trend(candles):
    directions = [float(candles[i-1]["close"]) > float(candles[i]["close"]) for i in range(1, 4)]
    return all(directions) or not any(directions)

def calculate_strength(rsi, volume_ok, trend_ok):
    strength = 0
    if volume_ok: strength += 30
    if trend_ok: strength += 40
    if 60 <= rsi <= 70 or 30 <= rsi <= 40: strength += 30
    return strength

def check_result(signal_time, action, symbol):
    time_dt = datetime.strptime(signal_time, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=1)
    candles = get_ohlc(symbol, count=2)
    for candle in candles:
        if candle["datetime"].startswith(time_dt.strftime("%Y-%m-%d %H:%M")):
            open_price = float(candle["open"])
            close_price = float(candle["close"])
            if action == "Buy" and close_price > open_price:
                return "✅ Win"
            elif action == "Sell" and close_price < open_price:
                return "✅ Win"
            else:
                return "❌ Loss"
    return "❌ No Data"

def generate_latest_signals():
    signals = []
    for symbol in SYMBOLS:
        candles = get_ohlc(symbol, count=20)
        if len(candles) < 15:
            continue
        latest, prev = candles[0], candles[1]
        volume_ok = float(latest["volume"]) > float(prev["volume"])
        rsi = calculate_rsi(candles[:15])
        trend_ok = detect_trend(candles[:4])
        if volume_ok or trend_ok:
            action = "Buy" if float(latest["close"]) > float(latest["open"]) else "Sell"
            strength = calculate_strength(rsi, volume_ok, trend_ok)
            if strength < 80:
                continue
            result = check_result(latest["datetime"], action, symbol)
            signals.append({
                "pair": symbol,
                "action": action,
                "strength": strength,
                "buy_time": latest["datetime"],
                "result": result
            })
    save_history(signals)
    return signals

def save_history(new_signals):
    try:
        with open("signal_history.json", "r") as f:
            history = json.load(f)
    except:
        history = []
    history.extend(new_signals)
    history = history[-100:]
    with open("signal_history.json", "w") as f:
        json.dump(history, f, indent=2)

def get_accuracy_stats():
    try:
        with open("signal_history.json", "r") as f:
            history = json.load(f)
    except:
        return {"accuracy": "N/A", "wins": 0, "losses": 0}
    wins = sum(1 for s in history if s.get("result") == "✅ Win")
    total = len(history)
    accuracy = f"{int((wins / total) * 100)}%" if total > 0 else "0%"
    return {"accuracy": accuracy, "wins": wins, "losses": total - wins}
