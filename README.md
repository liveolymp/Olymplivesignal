# Live Olymp Signal Engine

This is the backend engine that fetches real-time Forex data and applies:
- RSI filter (14)
- Volume spike
- Breakout detection
to deliver high-accuracy Buy/Sell signals (80%+ only).

## How to Run

```bash
npm install
node index.js
```

API will be available at:
```
http://localhost:3000/api/latest-signals
```

Auto-updates every 60 seconds.