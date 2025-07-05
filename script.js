const apiURL = "https://olymp-signal-backend.onrender.com/api/latest-signals";

async function loadSignals() {
  try {
    const res = await fetch(apiURL);
    const data = await res.json();
    const container = document.getElementById("signals");
    container.innerHTML = "";

    if (!data.signals || data.signals.length === 0) {
      container.innerHTML = "<div class='card'>No strong signals found.</div>";
      return;
    }

    data.signals.forEach(signal => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <div><strong>Pair:</strong> ${signal.pair}</div>
        <div><strong>Action:</strong> ${signal.action}</div>
        <div><strong>Strength:</strong> <span class="strength">${signal.strength}%</span></div>
        <div><strong>Buy Time:</strong> ${signal.buy_time}</div>
      `;
      container.appendChild(div);
    });
  } catch (err) {
    document.getElementById("signals").innerHTML = "<div class='card'>Error loading signal.</div>";
  }
}

loadSignals();
setInterval(loadSignals, 30000); // Auto-refresh every 30s