
const express = require('express');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;

app.use(cors());

const pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'];

function getRSI() {
  return 50 + Math.random() * 50;
}

function getVolume() {
  return 1000 + Math.random() * 2000;
}

function getBreakout() {
  return Math.random() < 0.4;
}

function generateSignal(pair) {
  const rsi = getRSI();
  const volume = getVolume();
  const breakout = getBreakout();

  if (rsi > 60 && volume > 1200 && breakout) {
    return {
      pair,
      action: 'BUY',
      entry: (1 + Math.random() * 0.01).toFixed(5),
      exit: (1 + Math.random() * 0.01).toFixed(5),
      strength: Math.floor(80 + Math.random() * 20) + '%',
      chart_url: `https://www.tradingview.com/chart/?symbol=${pair}`
    };
  } else if (rsi < 40 && volume > 1200 && breakout) {
    return {
      pair,
      action: 'SELL',
      entry: (1 + Math.random() * 0.01).toFixed(5),
      exit: (1 + Math.random() * 0.01).toFixed(5),
      strength: Math.floor(80 + Math.random() * 20) + '%',
      chart_url: `https://www.tradingview.com/chart/?symbol=${pair}`
    };
  } else {
    return null;
  }
}

let currentSignals = [];

function updateSignals() {
  currentSignals = [];
  pairs.forEach(pair => {
    const signal = generateSignal(pair);
    if (signal) currentSignals.push(signal);
  });
  console.log('Updated signals:', currentSignals);
}

updateSignals();
setInterval(updateSignals, 60000);

app.get('/api/latest-signals', (req, res) => {
  res.json(currentSignals);
});

app.listen(port, () => {
  console.log(`Olymp Signal Engine running on port ${port}`);
});
