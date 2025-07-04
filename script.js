
const PASSWORD = "221303";
const isAuthenticated = localStorage.getItem("authenticated") === "true";
const pwdScreen = document.getElementById("passwordScreen");
const introPopup = document.getElementById("introPopup");
const mainContent = document.getElementById("mainContent");
const pwdInput = document.getElementById("pwdInput");
const signalTable = document.querySelector("#signalTable tbody");
const refreshBtn = document.getElementById("refreshBtn");
const sound = document.getElementById("notificationSound");

function showIntro() {
  introPopup.style.display = "block";
  setTimeout(() => {
    introPopup.style.display = "none";
    mainContent.style.display = "block";
    loadSignals();
  }, 2500);
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

function loadSignals() {
  fetch("https://your-live-engine-url.com/api/latest-signals")  // Replace with real endpoint
    .then(res => res.json())
    .then(data => {
      signalTable.innerHTML = "";
      data.forEach(sig => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${sig.pair}</td>
          <td class="${sig.action === 'BUY' ? 'action-buy' : 'action-sell'}">${sig.action}</td>
          <td>${sig.entry}</td>
          <td>${sig.exit}</td>
          <td>${sig.strength}</td>
          <td><a href="${sig.chart_url}" target="_blank">🔍 View</a></td>`;
        signalTable.appendChild(row);
      });
      sound.play();
    });
}
