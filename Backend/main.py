from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client
import numpy as np
import talib
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Set up proxy session
session = requests.Session()
session.proxies = {
    'http': 'http://vfrutron:cqe8c72qjinn@38.154.227.167:5868',
    'https': 'http://vfrutron:cqe8c72qjinn@38.154.227.167:5868'
}

client = Client(API_KEY, API_SECRET, requests_params={"session": session})

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Olymp-compatible pairs
symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT",
    "BNBUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT",
    "EURUSDT", "GBPUSDT", "AUDUSDT", "JPYUSDT"
]

# Signal generation function
def generate_signal(symbol):
    try:
        klines = client.get_klines(symbol=symbol, interval="1m", limit=50)
        closes = [float(k[4]) for k in klines]
        volumes = [float(k[5]) for k in klines]

        if len(closes) < 20:
            return None

        rsi = talib.RSI(np.array(closes), timeperiod=14)[-1]
        volume_avg = sum(volumes[-10:]) / 10
        current_volume = volumes[-1]

        if rsi < 30 and current_volume > volume_avg:
            action = "BUY"
        elif rsi > 70 and current_volume > volume_avg:
            action = "SELL"
        else:
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

@app.get("/api/latest-signals")
def get_signals():
    output = []
    for symbol in symbols:
        try:
            signal = generate_signal(symbol)
            if signal:
                output.append(signal)
        except Exception as e:
            print(f"⚠️ Error on {symbol}: {e}")
    return {"signals": output}
