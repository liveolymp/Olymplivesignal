
async function fetchBinanceData(symbol) {
  const response = await fetch(`https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=1m&limit=100`);
  const data = await response.json();
  return data.map(k => parseFloat(k[4])); // Close prices
}

function calculateRSI(closes, period = 14) {
  let gains = 0, losses = 0;
  for (let i = 1; i <= period; i++) {
    const change = closes[i] - closes[i - 1];
    if (change >= 0) gains += change;
    else losses -= change;
  }
  const avgGain = gains / period;
  const avgLoss = losses / period;
  const rs = avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
}

function getTrend(closes) {
  const recent = closes.slice(-10);
  return recent[recent.length - 1] > recent[0] ? "Up" : "Down";
}

function formatAMPM(date) {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12 || 12;
  minutes = minutes < 10 ? '0'+minutes : minutes;
  return hours + ':' + minutes + ' ' + ampm;
}

async function updateSignal() {
  const time = new Date();
  document.getElementById('time').textContent = formatAMPM(time);

  const signals = [];

  const pairs = [
    { symbol: 'BTCUSDT', name: 'BTC/USDT' },
    { symbol: 'ETHUSDT', name: 'ETH/USDT' }
  ];

  for (let p of pairs) {
    try {
      const closes = await fetchBinanceData(p.symbol);
      const rsi = Math.round(calculateRSI(closes));
      const trend = getTrend(closes);
      const strength = Math.min(100, Math.max(50, trend === 'Up' ? rsi + 10 : 100 - rsi));
      const action = rsi > 60 ? 'BUY' : rsi < 40 ? 'SELL' : 'WAIT';

      if (strength >= 80 && action !== 'WAIT') {
        signals.push({
          name: p.name,
          action,
          rsi,
          trend,
          volume: "Estimated",
          strength
        });
      }
    } catch (e) {
      console.error("Error fetching data for", p.symbol, e);
    }
  }

  const container = document.getElementById('signals');
  container.innerHTML = '';
  if (signals.length === 0) {
    container.innerHTML = '<p>No strong signals right now. Refreshing...</p>';
  } else {
    for (let sig of signals) {
      const div = document.createElement('div');
      div.className = 'signal ' + (sig.action === 'BUY' ? 'buy' : 'sell');
      div.innerHTML = `
        <h3>${sig.name}</h3>
        <p><strong>Action:</strong> ${sig.action}</p>
        <p><strong>RSI:</strong> ${sig.rsi}</p>
        <p><strong>Trend:</strong> ${sig.trend}</p>
        <p><strong>Volume:</strong> ${sig.volume}</p>
        <p><strong>Strength:</strong> ${sig.strength}%</p>
      `;
      container.appendChild(div);
    }
  }
}

setInterval(updateSignal, 60000);
updateSignal();
