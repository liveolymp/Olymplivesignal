from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime
import numpy as np
from binance.client import Client
import os

app = FastAPI()

# CORS settings
origins = ["http://localhost", "https://liveolymp.github.io"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read Binance credentials from Railway environment
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

class Signal(BaseModel):
    pair: str
    action: str
    timeframe: str
    buy_time: str
    strength: int

class SignalsResponse(BaseModel):
    signals: List[Signal]

def get_current_ist_time():
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%H:%M:%S")

def calculate_rsi(close_prices, period=14):
    deltas = np.diff(close_prices)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(close_prices)
    rsi[:period] = 100. - 100. / (1. + rs)
    for i in range(period, len(close_prices)):
        delta = deltas[i - 1]
        upval = delta if delta > 0 else 0.
        downval = -delta if delta < 0 else 0.
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)
    return rsi

def fetch_candles(pair, interval='1m', limit=50):
    klines = client.get_klines(symbol=pair, interval=interval, limit=limit)
    closes = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]
    return closes, volumes, highs, lows

def detect_breakout(highs, lows):
    prev_high = np.mean(highs[:-1])
    prev_low = np.mean(lows[:-1])
    current_close = highs[-1]
    return current_close > prev_high, current_close < prev_low

def calculate_strength(rsi_value, volume_change, breakout):
    score = 0
    score += 40 if rsi_value > 70 or rsi_value < 30 else 20
    score += 30 if volume_change > 1.2 else 10
    score += 30 if breakout else 10
    return min(score, 100)

@app.get("/api/latest-signals", response_model=SignalsResponse)
async def latest_signals():
    pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]
    signals = []
    for pair in pairs:
        try:
            closes, volumes, highs, lows = fetch_candles(pair)
            rsi = calculate_rsi(np.array(closes))
            latest_rsi = rsi[-1]
            volume_change = volumes[-1] / volumes[-2] if volumes[-2] > 0 else 1
            breakout_up, breakout_down = detect_breakout(highs, lows)
            action = None
            strength = 0
            if latest_rsi < 30 and volume_change > 1.2 and breakout_up:
                action = "Buy"
                strength = calculate_strength(latest_rsi, volume_change, True)
            elif latest_rsi > 70 and volume_change > 1.2 and breakout_down:
                action = "Sell"
                strength = calculate_strength(latest_rsi, volume_change, True)
            if action:
                signals.append(Signal(
                    pair=pair,
                    action=action,
                    timeframe="1m",
                    buy_time=get_current_ist_time(),
                    strength=int(strength)
                ))
        except Exception as e:
            print(f"Error on {pair}: {e}")
    return SignalsResponse(signals=signals)
