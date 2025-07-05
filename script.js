const apiUrl = "https://olymp-signal-backend.onrender.com/api/latest-signals";

const strengthLabel = (strength) => {
  if (strength >= 81) return "strong";
  if (strength >= 51) return "moderate";
  return "weak";
};

async function fetchSignals() {
  const container = document.getElementById("signals");
  container.innerHTML = "Loading signals...";
  try {
    const res = await fetch(apiUrl);
    const data = await res.json();
    if (!data.signals || data.signals.length === 0) {
      container.innerHTML = "<p>No signals available.</p>";
      return;
    }
    container.innerHTML = "";
    data.signals.forEach(signal => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <p><strong>Pair:</strong> ${signal.pair}</p>
        <p><strong>Action:</strong> ${signal.action}</p>
        <p><strong>Timeframe:</strong> ${signal.timeframe}</p>
        <p><strong>Buy Time:</strong> ${signal.buy_time}</p>
        <p><strong>Strength:</strong> <span class="${strengthLabel(signal.strength)}">${signal.strength}%</span></p>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = "<p>Error loading signals. Please try again later.</p>";
  }
}

document.getElementById("refreshBtn").addEventListener("click", fetchSignals);
fetchSignals();
