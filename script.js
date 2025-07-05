const API = "https://olymp-signal-backend.up.railway.app/api/latest-signals";

async function loadSignals() {
  const output = document.getElementById("output");
  output.innerHTML = "Loading...";
  try {
    const res = await fetch(API);
    const data = await res.json();
    if (!data.signals || data.signals.length === 0) {
      output.innerHTML = "<p>No signals available at the moment.</p>";
      return;
    }
    output.innerHTML = "";
    data.signals.forEach(signal => {
      const level = signal.strength >= 80 ? 'strong' : signal.strength >= 50 ? 'moderate' : 'weak';
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <h3>${signal.pair} - <span class="${level}">${signal.action}</span></h3>
        <p><strong>Buy Time (IST):</strong> ${signal.buy_time}</p>
        <p><strong>Timeframe:</strong> ${signal.timeframe}</p>
        <p><strong>Strength:</strong> <span class="${level}">${signal.strength}%</span></p>
      `;
      output.appendChild(card);
    });
  } catch (err) {
    output.innerHTML = "<p style='color:red;'>Error fetching signals. Please try again later.</p>";
    console.error(err);
  }
}
loadSignals();
