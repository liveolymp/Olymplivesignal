// script.js

const API_URL = "https://your-backend-domain.com/api/latest-signals"; // Change to your real backend URL

const signalContainer = document.getElementById("signal-container");

async function fetchSignals() {
  signalContainer.innerHTML = "<p>Loading signals...</p>";
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error("Failed to fetch signals");

    const data = await res.json();
    renderSignals(data.signals || []);
  } catch (err) {
    signalContainer.innerHTML = `<p style="color: #f87171;">Error loading signals. Retrying in 10 seconds...</p>`;
    setTimeout(fetchSignals, 10000);
  }
}

function renderSignals(signals) {
  if (signals.length === 0) {
    signalContainer.innerHTML = "<p>No signals available right now.</p>";
    return;
  }

  signalContainer.innerHTML = "";

  signals.forEach((signal) => {
    const card = document.createElement("div");
    card.className = "signal-card";

    const strengthClass =
      signal.strength >= 81
        ? "strength-high"
        : signal.strength >= 51
        ? "strength-medium"
        : "strength-low";

    card.innerHTML = `
      <h3>${signal.pair} — ${signal.action}</h3>
      <p><strong>Timeframe:</strong> ${signal.timeframe}</p>
      <p><strong>Buy Time (IST):</strong> ${signal.buy_time}</p>
      <p><strong>Strength:</strong> <span class="signal-strength ${strengthClass}">${signal.strength}%</span></p>
    `;

    signalContainer.appendChild(card);
  });
}

// Auto-refresh every 60 seconds
setInterval(fetchSignals, 60000);

fetchSignals();
