const API_URL = "https://olymp-signal-backend.up.railway.app/api/latest-signals";

async function loadSignals() {
  const container = document.getElementById("signal-container");
  container.innerHTML = "Loading...";
  try {
    const res = await fetch(API_URL);
    const data = await res.json();
    if (data.signals.length === 0) {
      container.innerHTML = "<p>No signals right now.</p>";
      return;
    }
    container.innerHTML = "";
    data.signals.forEach(sig => {
      const strengthClass = sig.strength >= 80 ? "strong" : sig.strength >= 50 ? "moderate" : "weak";
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <h2>${sig.pair} - <span class="${strengthClass}">${sig.action}</span></h2>
        <p><strong>Timeframe:</strong> ${sig.timeframe}</p>
        <p><strong>Buy Time (IST):</strong> ${sig.buy_time}</p>
        <p><strong>Strength:</strong> <span class="${strengthClass}">${sig.strength}%</span></p>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = "<p style='color:red;'>Error loading signals.</p>";
  }
}
loadSignals();
