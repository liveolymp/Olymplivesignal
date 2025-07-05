from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client
import numpy as np
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Proxy setup (optional)
session = requests.Session()
session.proxies = {
    'http': 'http://vfrutron:cqe8c72qjinn@38.154.227.167:5868',
    'https': 'http://vfrutron:cqe8c72qjinn@38.154.227.167:5868'
}

# Binance client with proxy
client = Client(
    API_KEY,
    API_SECRET,
    requests_params={
        "proxies": {
            "http": "http://vfrutron:cqe8c72qjinn@38.154.227.167:5868",
            "https": "http://vfrutron:cqe8c72qjinn@38.154.227.167:5868"
        }
    }
)

app = FastAPI()

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Olymp Trade compatible pairs
symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT",
    "BNBUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT",
    "EURUSDT", "GBPUSDT", "AUDUSDT", "JPYUSDT"
]

# Pure Python RSI calculation
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

# Signal logic
def generate_signal(symbol):
    try:
        klines = client.get_klines(symbol=symbol, interval="1m", limit=50)
        closes = [float(k[4]) for k in klines]
        volumes = [float(k[5]) for k in klines]

        if len(closes) < 20:
            return None

        rsi_series = calculate_rsi(closes)[-1]
        volume_avg = sum(volumes[-10:]) / 10
        current_volume = volumes[-1]

        if rsi_series < 30 and current_volume > volume_avg:
            action = "BUY"
        elif rsi_series > 70 and current_volume > volume_avg:
            action = "SELL"
        else:
            return None

        strength = int(min(abs(rsi_series - 50) + (current_volume / volume_avg) * 10, 100))

        return {
            "pair": symbol.replace("USDT", "/USDT"),
            "action": action,
            "strength": strength,
            "timeframe": "1m",
            "buy_time": datetime.now().strftime("%I:%M %p")
        }

    except Exception as e:
        print(f"❗ Error in {symbol}: {e}")
        return None

@app.get("/api/latest-signals")
def get_signals():
    output = []
    for symbol in symbols:
        try:
            result = generate_signal(symbol)
            if result:
                output.append(result)
        except Exception as e:
            print(f"⚠️ Error on {symbol}: {e}")
    return {"signals": output}
