from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("TWELVEDATA_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Olymp/Binomo common pairs
symbols = ["EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD", "ETH/USD", "XAU/USD"]

def fetch_signal(symbol):
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={symbol.replace('/', '')}&interval=1min&outputsize=50&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if "values" not in data:
            return None

        closes = [float(c["close"]) for c in data["values"]]
        volumes = [float(c["volume"]) for c in data["values"]]
        if len(closes) < 15:
            return None

        gains, losses = [], []
        for i in range(1, 15):
            diff = closes[i - 1] - closes[i]
            if diff > 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))
        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))

        avg_vol = sum(volumes[:10]) / 10
        current_vol = volumes[0]

        if rsi < 30 and current_vol > avg_vol:
            action = "BUY"
        elif rsi > 70 and current_vol > avg_vol:
            action = "SELL"
        else:
            return None

        strength = min(int(abs(rsi - 50) + (current_vol / avg_vol) * 10), 100)
        if strength < 80:
            return None

        return {
            "pair": symbol,
            "action": action,
            "strength": strength,
            "timeframe": "1m",
            "buy_time": datetime.utcnow().strftime("%I:%M %p")
        }
    except:
        return None

@app.get("/api/latest-signals")
def get_signals():
    signals = []
    for symbol in symbols:
        sig = fetch_signal(symbol)
        if sig:
            signals.append(sig)
        if len(signals) >= 2:
            break
    return {"signals": signals}
