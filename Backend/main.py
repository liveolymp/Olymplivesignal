from fastapi import FastAPI
from generate_signals import generate_latest_signals

app = FastAPI()

@app.get("/")
def root():
    return {"message": "✅ Olymp Signal API is running with MACD + EMA filters"}

@app.get("/api/latest-signals")
def get_signals():
    signals = generate_latest_signals()
    return {"signals": signals}
