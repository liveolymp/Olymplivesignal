
function formatAMPM(date) {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12;
  minutes = minutes < 10 ? '0'+minutes : minutes;
  return hours + ':' + minutes + ' ' + ampm;
}

function updateTime() {
  const now = new Date();
  document.getElementById('time').textContent = formatAMPM(now);
}

function fetchSignals() {
  // Placeholder sample signals
  const signals = [
    { pair: 'EUR/USD', action: 'BUY', rsi: 65, volume: 'High', trend: 'Up', strength: 91 },
    { pair: 'GBP/USD', action: 'SELL', rsi: 45, volume: 'Medium', trend: 'Down', strength: 83 },
  ];

  const container = document.getElementById('signals');
  container.innerHTML = '';
  signals.forEach(sig => {
    const div = document.createElement('div');
    div.className = 'signal ' + (sig.action === 'BUY' ? 'buy' : 'sell');
    div.innerHTML = `
      <h3>${sig.pair}</h3>
      <p><strong>Action:</strong> ${sig.action}</p>
      <p><strong>RSI:</strong> ${sig.rsi}</p>
      <p><strong>Trend:</strong> ${sig.trend}</p>
      <p><strong>Volume:</strong> ${sig.volume}</p>
      <p><strong>Strength:</strong> ${sig.strength}%</p>
    `;
    container.appendChild(div);
  });
}

setInterval(updateTime, 1000);
setInterval(fetchSignals, 60000);
updateTime();
fetchSignals();
