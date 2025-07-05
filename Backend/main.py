from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client
import numpy as np
import talib
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Load .env credentials
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Proxy setup (change this to your latest one if needed)
session = requests.Session()
session.proxies = {
    'http': 'http://vfrutron:cqe8c72qjinn@38.154.227.167:5868',
    'https': 'http://vfrutron:cqe8c72qjinn@38.154.227.167:5868'
}

client = Client(API_KEY, API_SECRET, requests_params={"session": session})

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Olymp Trade compatible pairs (Binance format)
symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT",
    "BNBUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT",
    "EURUSDT", "GBPUSDT", "AUDUSDT", "JPYUSDT"
]

# Signal logic
def generate_signal(symbol):
    try:
        klines = client.get_klines(symbol=symbol, interval="1m", limit=50)
        closes = [float(k[4]) for k in klines]
        volumes = [float(k[5]) for k in klines]

        if len(closes) < 20:
            print(f"⚠️ Not enough data for {symbol}")
            return None

        rsi = talib.RSI(np.array(closes), timeperiod=14)[-1]
        volume_avg = sum(volumes[-10:]) / 10
        current_volume = volumes[-1]

        if rsi < 30 and current_volume > volume_avg:
            action = "BUY"
        elif rsi > 70 and current_volume > volume_avg:
            action = "SELL"
        else:
            print(f"❌ No signal for {symbol}")
            return None

        strength = int(min(abs(rsi - 50) + (current_volume / volume_avg) * 10, 100))

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

# API Endpoint
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
