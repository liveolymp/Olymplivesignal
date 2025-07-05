const apiURL = "https://olymp-signal-backend.onrender.com/api/latest-signals";
async function fetchSignals() {
  try {
    const res = await fetch(API_URL);
    const data = await res.json();
    const container = document.getElementById("signal-container");
    const now = new Date().toLocaleTimeString();
    document.getElementById("updated-time").innerText = "Last updated: " + now;

    // Filter only signals with strength ≥ 65
    const strongSignals = data.signals
      .filter(signal => signal.strength >= 65)
      .slice(0, 2); // Show max 2

    container.innerHTML = "";

    if (strongSignals.length === 0) {
      container.innerHTML = "<p>No strong signals (≥65%) at the moment.</p>";
      return;
    }

    strongSignals.forEach((signal) => {
      const div = document.createElement("div");
      let color = "yellow";
      if (signal.strength >= 80) color = "green";
      else if (signal.strength <= 50) color = "red";
      div.className = "card " + color;
      div.innerHTML = `
        <h2>${signal.pair}</h2>
        <p>Action: <strong>${signal.action}</strong></p>
        <p>Timeframe: ${signal.timeframe}</p>
        <p>Buy Time: ${signal.buy_time}</p>
        <p>Strength: ${signal.strength}%</p>
      `;
      container.appendChild(div);
    });

  } catch (err) {
    document.getElementById("signal-container").innerText = "⚠️ Error loading signal.";
  }
}

fetchSignals();
setInterval(fetchSignals, 30000);
