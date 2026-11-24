// Hauptmenü: weiter zum Spiel, abmelden oder Spielstand zurücksetzen (mit Bestätigung).

const dialog = document.getElementById("bestaetigung");
const meldung = document.getElementById("meldung");

function begruessungFuellen(stand) {
  document.getElementById("benutzername").textContent = stand.benutzername;
  document.getElementById("rang").textContent = stand.rang;
  // Easteregg: goldener Cookie, wenn der Code schon gefunden wurde
  document.body.classList.toggle("golden", stand.erleuchtet);
}

anfrage("/api/spiel/stand").then(begruessungFuellen);

document.getElementById("zum-spiel").addEventListener("click", () => {
  window.location.href = "/spiel";
});

document.getElementById("abmelden").addEventListener("click", async () => {
  const antwort = await anfrage("/api/konto/abmelden", {});
  window.location.href = antwort.weiter;
});

document.getElementById("zuruecksetzen").addEventListener("click", () => dialog.showModal());
document.getElementById("abbrechen").addEventListener("click", () => dialog.close());

document.getElementById("ja-zuruecksetzen").addEventListener("click", async () => {
  dialog.close();
  begruessungFuellen(await anfrage("/api/spiel/zuruecksetzen", {}));
  meldung.textContent = "Spielstand wurde zurückgesetzt.";
});
