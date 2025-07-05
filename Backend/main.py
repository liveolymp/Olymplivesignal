from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client
import os
import statistics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load keys from environment
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def calculate_rsi(prices, period=14):
    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0)
        else:
            losses.append(-diff)
            gains.append(0)
    if not gains or not losses:
        return 50
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def generate_signal(pair="BTCUSDT", interval="1m"):
    candles = client.get_klines(symbol=pair, interval=interval, limit=50)
    closes = [float(c[4]) for c in candles]
    volumes = [float(c[5]) for c in candles]
    times = [c[0] for c in candles]

    rsi = calculate_rsi(closes)
    avg_vol = statistics.mean(volumes)
    latest_vol = volumes[-1]
    strength = min(100, max(0, int((latest_vol / avg_vol) * 100))) if avg_vol != 0 else 0

    action = "HOLD"
    if rsi < 30:
        action = "BUY"
    elif rsi > 70:
        action = "SELL"

    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    return {
        "pair": pair.replace("USDT", "/USDT"),
        "action": action,
        "timeframe": interval,
        "buy_time": now.strftime("%I:%M %p"),
        "strength": strength
    }

@app.get("/")
def root():
    return {"message": "Olymp Signal backend live"}

@app.get("/api/latest-signals")
def get_signals():
    pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    signals = [generate_signal(pair=p) for p in pairs]
    return {"signals": signals}
