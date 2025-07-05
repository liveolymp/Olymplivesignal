from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# 🆕 New working proxy (tested):
client = Client(
    API_KEY,
    API_SECRET,
    requests_params={
        "proxies": {
            "http": "http://proxyuser:proxypass@146.190.65.20:8080",
            "https": "http://proxyuser:proxypass@146.190.65.20:8080"
        }
    }
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "EURUSDT", "GBPUSDT"]

def calculate_rsi(prices, period=14):
    prices = np.array(prices)
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)
    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        gain = max(delta, 0)
        loss = -min(delta, 0)
        up = (up * (period - 1) + gain) / period
        down = (down * (period - 1) + loss) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)
    return rsi

def generate_signal(symbol):
    try:
        klines = client.get_klines(symbol=symbol, interval="1m", limit=50)
        closes = [float(k[4]) for k in klines]
        volumes = [float(k[5]) for k in klines]
        if len(closes) < 20:
            return None
        rsi = calculate_rsi(closes)[-1]
        avg_vol = sum(volumes[-10:]) / 10
        curr_vol = volumes[-1]
        if rsi < 30 and curr_vol > avg_vol:
            action = "BUY"
        elif rsi > 70 and curr_vol > avg_vol:
            action = "SELL"
        else:
            return None
        strength = min(int(abs(rsi - 50) + (curr_vol / avg_vol) * 10), 100)
        return {
            "pair": symbol.replace("USDT", "/USDT"),
            "action": action,
            "strength": strength,
            "timeframe": "1m",
            "buy_time": datetime.utcnow().strftime("%I:%M %p")
        }
    except Exception as e:
        print(f"Error on {symbol}:", e)
        return None

@app.get("/api/latest-signals")
def get_signals():
    signals = []
    for s in symbols:
        sig = generate_signal(s)
        if sig: signals.append(sig)
    return {"signals": signals}
