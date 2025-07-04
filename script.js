
async function fetchSignals() {
  try {
    const res = await fetch('http://localhost:3000/api/latest-signals');
    const data = await res.json();
    const container = document.getElementById('signalContainer');
    container.innerHTML = '';
    if (data.length === 0) {
      container.innerHTML = '<p>No signals available right now.</p>';
      return;
    }
    data.forEach(signal => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <h3>${signal.pair}</h3>
        <p>Action: <span class="${signal.action === 'BUY' ? 'green' : 'red'}">${signal.action}</span></p>
        <p>Entry: ${signal.entry}</p>
        <p>Exit: ${signal.exit}</p>
        <p>Strength: ${signal.strength}</p>
        <a href="${signal.chart_url}" target="_blank">📈 View Chart</a>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    document.getElementById('signalContainer').innerHTML = '<p>Error loading signals.</p>';
    console.error(err);
  }
}

document.getElementById('refreshBtn').addEventListener('click', fetchSignals);
setInterval(fetchSignals, 60000);
fetchSignals();
