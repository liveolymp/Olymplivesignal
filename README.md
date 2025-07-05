# Olymp Signal Backend

Live trading signal backend using Binance API and FastAPI.

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Set environment variables:
   export BINANCE_API_KEY=your_api_key
   export BINANCE_API_SECRET=your_secret

3. Run server:
   uvicorn main:app --host 0.0.0.0 --port 8000

## API
- GET /api/latest-signals → Live trading signals (Buy/Sell + Strength)
