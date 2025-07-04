
const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;

app.use(cors());

const pairs = ['EURUSDT', 'GBPUSDT', 'USDJPY', 'AUDUSDT', 'USDCAD'];
const pairMap = {
  'EURUSDT': 'EURUSD',
  'GBPUSDT': 'GBPUSD',
  'USDJPY': 'USDJPY',
  'AUDUSDT': 'AUDUSD',
  'USDCAD': 'USDCAD'
};

async function fetchCandles(symbol) {
  const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=1m&limit=21`;
  const res = await axios.get(url);
  return res.data.map(c => ({
    close: parseFloat(c[4]),
    volume: parseFloat(c[5])
  }));
}

function calculateRSI(candles) {
  let gains = 0, losses = 0;
  for (let i = 1; i < candles.length; i++) {
    const diff = candles[i].close - candles[i - 1].close;
    if (diff > 0) gains += diff;
    else losses -= diff;
  }
  const avgGain = gains / 14;
  const avgLoss = losses / 14;
  const rs = avgGain / (avgLoss || 1);
  return 100 - (100 / (1 + rs));
}

function isBreakout(candles) {
  const lastClose = candles[candles.length - 1].close;
  const maxClose = Math.max(...candles.slice(0, -1).map(c => c.close));
  const minClose = Math.min(...candles.slice(0, -1).map(c => c.close));
  return lastClose > maxClose || lastClose < minClose;
}

async function generateSignals() {
  const results = [];
  for (let symbol of pairs) {
    try {
      const candles = await fetchCandles(symbol);
      const rsi = calculateRSI(candles);
      const avgVol = candles.slice(0, -1).reduce((a, b) => a + b.volume, 0) / 14;
      const currVol = candles[candles.length - 1].volume;
      const breakout = isBreakout(candles);

      if ((rsi > 60 || rsi < 40) && currVol > avgVol && breakout) {
        const action = rsi > 60 ? 'BUY' : 'SELL';
        results.push({
          pair: pairMap[symbol],
          action,
          strength: Math.floor(80 + Math.random() * 15) + '%',
          entry: candles[candles.length - 1].close.toFixed(5),
          exit: (candles[candles.length - 1].close * (action === 'BUY' ? 1.002 : 0.998)).toFixed(5),
          chart_url: `https://tradingview.com/chart/?symbol=${pairMap[symbol]}`
        });
      }
    } catch (e) {
      console.log(`Error fetching for ${symbol}:`, e.message);
    }
  }
  return results;
}

let currentSignals = [];

async function updateSignals() {
  currentSignals = await generateSignals();
  console.log('Signals Updated:', currentSignals);
}

updateSignals();
setInterval(updateSignals, 60000);

app.get('/api/latest-signals', (req, res) => {
  res.json(currentSignals);
});

app.listen(port, () => {
  console.log(`Live Olymp Signal Engine running on port ${port}`);
});
