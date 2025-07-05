from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, statistics
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_klines(symbol="BTCUSDT", interval="1m", limit=50):
    url = "https://testnet.binance.vision/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def calculate_rsi(closes, period=14):
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def generate_signal(symbol):
    klines = get_klines(symbol=symbol)
    closes = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]
    rsi = calculate_rsi(closes)
    avg_vol = statistics.mean(volumes)
    strength = min(100, int((volumes[-1] / avg_vol) * 100)) if avg_vol else 0
    action = "HOLD"
    if rsi < 30: action = "BUY"
    elif rsi > 70: action = "SELL"
    ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
    return {
        "pair": symbol.replace("USDT", "/USDT"),
        "action": action,
        "timeframe": "1m",
        "buy_time": ist_time.strftime("%I:%M %p"),
        "strength": strength
    }

@app.get("/")
def root():
    return {"message": "Olymp Signal (Testnet) backend live"}

@app.get("/api/latest-signals")
def get_signals():
    symbols = [
  "EURUSDT", "GBPUSDT", "JPYUSDT", "AUDUSDT", "CADUSDT", "CHFUSDT", "NZDUSDT",
  "BTCUSDT", "ETHUSDT", "LTCUSDT", "XRPUSDT", "BCHUSDT", "ETCUSDT", "EOSUSDT",
  "DOTUSDT", "LINKUSDT", "TRXUSDT", "CRVUSDT", "XAUSDT", "XAGUSDT"
    ]
@app.get("/api/latest-signals")
def get_signals():
    output = []
    for symbol in symbols:
        try:
            result = generate_signal(symbol)
            output.append(result)
        except Exception as e:
            print(f"Error on {symbol}: {e}")
    return {"signals": output}
