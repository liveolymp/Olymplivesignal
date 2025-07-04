const SIGNAL_DURATION = 2 * 60 * 1000; // 2 minutes

function formatTime(date) {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  const ampm = hours >= 12 ? 'AM' : 'PM';
  hours = hours % 12 || 12;
  minutes = minutes < 10 ? '0' + minutes : minutes;
  return hours + ':' + minutes + ' ' + ampm;
}

function updateTimeDisplay() {
  document.getElementById('time').textContent = formatTime(new Date());
}

function toggleDarkMode() {
  document.body.classList.toggle('dark');
}

document.getElementById('mode-toggle').addEventListener('click', toggleDarkMode);

async function fetchBinanceData(symbol) {
  const res = await fetch(`https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=1m&limit=100`);
  const json = await res.json();
  return json.map(k => parseFloat(k[4]));
}

function calculateRSI(closes, period = 14) {
  let gains = 0, losses = 0;
  for (let i = 1; i <= period; i++) {
    const diff = closes[i] - closes[i - 1];
    if (diff >= 0) gains += diff;
    else losses -= diff;
  }
  const avgGain = gains / period;
  const avgLoss = losses / period;
  const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
}

function getTrend(closes) {
  const last = closes.slice(-10);
  return last[last.length - 1] > last[0] ? "Up" : "Down";
}

let lastSignals = {};

async function updateSignals() {
  updateTimeDisplay();
  const pairs = [
    { symbol: 'BTCUSDT', name: 'BTC/USDT' },
    { symbol: 'ETHUSDT', name: 'ETH/USDT' },
    { symbol: 'BNBUSDT', name: 'BNB/USDT' },
    { symbol: 'XRPUSDT', name: 'XRP/USDT' },
    { symbol: 'LTCUSDT', name: 'LTC/USDT' }
  ];

  const box = document.getElementById('signals');
  box.innerHTML = '';

  for (let pair of pairs) {
    try {
      const prices = await fetchBinanceData(pair.symbol);
      const rsi = Math.round(calculateRSI(prices));
      const trend = getTrend(prices);
      const strength = Math.min(100, Math.max(50, trend === 'Up' ? rsi + 10 : 100 - rsi));
      const action = rsi > 60 ? 'BUY' : rsi < 40 ? 'SELL' : 'WAIT';

      if (strength >= 80 && action !== 'WAIT') {
        const now = new Date();
        const entryTime = formatTime(now);
        const exitTime = formatTime(new Date(now.getTime() + SIGNAL_DURATION));

        if (!lastSignals[pair.symbol] || lastSignals[pair.symbol].entryTime !== entryTime) {
          document.getElementById('alertSound').play();
        }

        const strengthColor = strength > 90 ? '🟢' : strength >= 80 ? '🟡' : '🔴';

        const div = document.createElement('div');
        div.className = 'signal';
        div.innerHTML = `
          <h3>${pair.name}</h3>
          <p><strong>Action:</strong> ${action}</p>
          <p><strong>Buy Time:</strong> ${entryTime}</p>
          <p><strong>Exit Time:</strong> ${exitTime}</p>
          <p><strong>Trend:</strong> ${trend}</p>
          <p><strong>RSI:</strong> ${rsi}</p>
          <p><strong>Strength:</strong> ${strengthColor} ${strength}%</p>
        `;
        box.appendChild(div);

        lastSignals[pair.symbol] = {
          entryTime,
          exitTime,
          action
        };
      }
    } catch (err) {
      console.error("Error on", pair.symbol, err);
    }
  }
}

setInterval(updateSignals, 60000);
updateSignals();
updateTimeDisplay();
