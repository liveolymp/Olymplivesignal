
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
  pwdScreen.style.display = "none";
  showIntro(); // <- this shows intro and then loads main content
}
