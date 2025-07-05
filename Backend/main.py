from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TWELVEDATA_API_KEY")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

symbols = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF", "BTC/USD", "ETH/USD", "XAU/USD"]

def get_rsi(closes):
    gains, losses = [], []
    for i in range(1, 15):
        diff = closes[i - 1] - closes[i]
        gains.append(diff if diff > 0 else 0)
        losses.append(abs(diff) if diff < 0 else 0)
    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14 or 0.0001
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def fetch_signal(symbol):
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={symbol.replace('/', '')}&interval=1min&outputsize=50&apikey={API_KEY}"
        data = requests.get(url).json()
        if "values" not in data:
            return None

        values = data["values"]
        closes = [float(i["close"]) for i in values]
        volumes = [float(i["volume"]) for i in values]
        highs = [float(i["high"]) for i in values]

        rsi = get_rsi(closes)
        avg_vol = sum(volumes[1:11]) / 10
        vol_spike = volumes[0] > avg_vol

        ma = sum(closes[1:21]) / 20
        trend = "up" if closes[0] > ma else "down" if closes[0] < ma else "flat"

        recent_high = max(highs[1:6])
        breakout = float(values[0]["high"]) > recent_high

        if rsi < 30 and vol_spike and trend == "up" and breakout:
            action = "BUY"
        elif rsi > 70 and vol_spike and trend == "down" and breakout:
            action = "SELL"
        else:
            return None

        strength = min(int(abs(rsi - 50) + (volumes[0] / avg_vol) * 10), 100)
        if strength < 80:
            return None

        return {
            "pair": symbol,
            "action": action,
            "strength": strength,
            "buy_time": datetime.utcnow().strftime("%I:%M %p"),
            "trend": trend,
            "rsi": rsi,
            "volume_spike": vol_spike
        }
    except:
        return None

@app.get("/api/latest-signals")
def get_signals():
    results = []
    for s in symbols:
        sig = fetch_signal(s)
        if sig:
            results.append(sig)
        if len(results) >= 2:
            break
    return { "signals": results }