(async () => {
  try {
    const res = await fetch('signals.json', { cache: 'no-store' });
    const data = await res.json();
    const latest = data.signals && data.signals[0];

    const container = document.getElementById('signal-container');
    if (!latest) {
      container.innerHTML = '<p>No signal data found.</p>';
      return;
    }

    container.innerHTML = `
      <h2>${latest.forex}</h2>
      <p><strong>${latest.type}</strong> signal &ndash; ${latest.strength}% confidence</p>
      <p>Entry Time: ${latest.entry_time}</p>
      <p>Time Frame: ${latest.timeframe}</p>
    `;
  } catch (err) {
    console.error(err);
    document.getElementById('signal-container').innerHTML = '<p>Error loading signal.</p>';
  }
})();
