# Olymp Signal Backend (TwelveData Version)

Live Forex/Crypto signal engine using RSI + Volume logic.

## Setup

1. Copy `.env.example` → `.env`
2. Replace with your TwelveData API key

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
