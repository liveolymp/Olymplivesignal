const PASSWORD = "221303";
const pwdScreen = document.getElementById("passwordScreen");
const introPopup = document.getElementById("introPopup");
const mainContent = document.getElementById("mainContent");
const pwdInput = document.getElementById("pwdInput");
const signalCards = document.getElementById("signalCards");
const refreshBtn = document.getElementById("refreshBtn");

function showIntro() {
  introPopup.style.display = "block";
  setTimeout(() => {
    introPopup.style.display = "none";
    mainContent.style.display = "block";
    loadSignals();
  }, 2000);
}

function authenticateAndStart() {
  pwdScreen.style.display = "none";
  localStorage.setItem("authenticated", "true");
  showIntro();
}

if (localStorage.getItem("authenticated") === "true") {
  authenticateAndStart();
} else {
  pwdScreen.style.display = "flex";
  pwdInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
      if (pwdInput.value === PASSWORD) {
        authenticateAndStart();
      } else {
        alert("Wrong Password!");
        pwdInput.value = "";
      }
    }
  });
}

refreshBtn.onclick = loadSignals;
setInterval(loadSignals, 10000);

function loadSignals() {
  const rsiFilter = document.getElementById("rsiFilter").checked;
  const volumeFilter = document.getElementById("volumeFilter").checked;
  const breakoutFilter = document.getElementById("breakoutFilter").checked;

  fetch("https://live.olympsignalapi.in/api/latest-signals")
    .then(res => res.json())
    .then(data => {
      signalCards.innerHTML = "";
      // You can add filtering based on rsiFilter, volumeFilter, breakoutFilter here if needed
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
    })
    .catch(() => console.error("Signal fetch failed."));
}
