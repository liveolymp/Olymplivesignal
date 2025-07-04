
const PASSWORD = "221303";
const isAuthenticated = localStorage.getItem("authenticated") === "true";
const pwdScreen = document.getElementById("passwordScreen");
const introPopup = document.getElementById("introPopup");
const mainContent = document.getElementById("mainContent");
const pwdInput = document.getElementById("pwdInput");
const signalCards = document.getElementById("signalCards");
const refreshBtn = document.getElementById("refreshBtn");
const sound = document.getElementById("notificationSound");

function showIntro() {
  introPopup.style.display = "block";
  setTimeout(() => {
    introPopup.style.display = "none";
    mainContent.style.display = "block";
    loadSignals();
  }, 2000);
}

if (!isAuthenticated) {
  pwdScreen.style.display = "flex";
  pwdInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter" && pwdInput.value === PASSWORD) {
      localStorage.setItem("authenticated", "true");
      pwdScreen.style.display = "none";
      showIntro();
    } else if (e.key === "Enter") {
      alert("Wrong Password!");
      pwdInput.value = "";
    }
  });
} else {
  mainContent.style.display = "block";
  loadSignals();
}

refreshBtn.onclick = loadSignals;
setInterval(loadSignals, 10000); // auto-refresh every 10 sec

function loadSignals() {
  fetch("https://live.olympsignalapi.in/api/latest-signals")
    .then(res => res.json())
    .then(data => {
      signalCards.innerHTML = "";
      data.forEach(sig => {
        const div = document.createElement("div");
        div.className = "signal-card";
        div.innerHTML = `
          <h3>${sig.pair}</h3>
          <p><strong>Action:</strong> <span class="${sig.action === 'BUY' ? 'action-buy' : 'action-sell'}">${sig.action}</span></p>
          <p><strong>Entry:</strong> ${sig.entry}</p>
          <p><strong>Exit:</strong> ${sig.exit}</p>
          <p><strong>Strength:</strong> ${sig.strength}</p>
          <p><a href="${sig.chart_url}" target="_blank">🔍 View Chart</a></p>
        `;
        signalCards.appendChild(div);
      });
      if (data.length > 0) sound.play();
    })
    .catch(() => console.error("Failed to fetch signals."));
}
