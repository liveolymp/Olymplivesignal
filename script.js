
const PASSWORD = "221303";
const passwordScreen = document.getElementById("passwordScreen");
const introPopup = document.getElementById("introPopup");
const mainContent = document.getElementById("mainContent");
const pwdInput = document.getElementById("pwdInput");
const signalTable = document.querySelector("#signalTable tbody");
const notificationSound = document.getElementById("notificationSound");

pwdInput.addEventListener("keyup", function(e) {
  if (e.key === "Enter") {
    if (pwdInput.value === PASSWORD) {
      passwordScreen.style.display = "none";
      introPopup.style.display = "block";
      setTimeout(() => {
        introPopup.style.display = "none";
        mainContent.style.display = "block";
        fetchSignals();
      }, 2500);
    } else {
      alert("Wrong password!");
      pwdInput.value = "";
    }
  }
});

function fetchSignals() {
  const dummySignals = [
    { pair: "EUR/USD", action: "BUY", entry: "12:01", exit: "12:04", strength: "85%" },
    { pair: "GBP/JPY", action: "SELL", entry: "12:03", exit: "12:06", strength: "90%" },
    { pair: "USD/INR", action: "BUY", entry: "12:05", exit: "12:08", strength: "88%" },
  ];
  renderSignals(dummySignals);
  notificationSound.play();
}

function renderSignals(signals) {
  signalTable.innerHTML = "";
  signals.forEach(sig => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${sig.pair}</td>
      <td class="${sig.action === 'BUY' ? 'action-buy' : 'action-sell'}">${sig.action}</td>
      <td>${sig.entry}</td>
      <td>${sig.exit}</td>
      <td>${sig.strength}</td>
    `;
    signalTable.appendChild(row);
  });
}
