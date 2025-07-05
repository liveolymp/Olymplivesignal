from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Olymp Signal backend running"}

@app.get("/api/latest-signals")
def get_signals():
    # Placeholder example signal
    return {
        "signals": [
            {
                "pair": "BTC/USDT",
                "action": "BUY",
                "timeframe": "1m",
                "buy_time": "12:30 PM",
                "strength": 87
            }
        ]
    }
