// Infotafel unten auf der Klickseite.
// Der Inhalt ist austauschbar: einfach weitere Einträge {titel, html} in INFO_INHALTE ergänzen.
// Die Punkte rechts oben zeigen, welcher Eintrag zu sehen ist. Gewechselt wird per Klick
// auf einen Punkt oder automatisch alle INFO_WECHSEL_SEKUNDEN.

const INFO_WECHSEL_SEKUNDEN = 20;

function schritte(liste) {
  return '<div class="schritte">' + liste.map(([nummer, titel, text]) =>
    `<div class="schritt"><span class="nummer">${nummer}</span><div><h3>${titel}</h3><p>${text}</p></div></div>`
  ).join("") + "</div>";
}

const INFO_INHALTE = [
  {
    titel: "So funktioniert Mathecookie",
    html: schritte([
      ["1", "Cookies sammeln", "Sammle Cookies mit einem Klick auf den großen Mathecookie."],
      ["2", "Mathecookie verbessern", "Verbessere die Menge deiner gesammelten Cookies pro Klick, indem du Aufgaben löst."],
      ["3", "Dein Weg des Mathecookies", "Steige in den Rängen auf und werde vom Mathecookie erleuchtet!"],
    ]),
  },
  {
    titel: "Gut zu wissen",
    html: schritte([
      ["!", "Falsch ist nicht teuer", "Nach einer falschen Antwort bleibt der Preis gleich. Teurer wird es nur, wenn du richtig liegst."],
      ["+", "Es wird schwerer", "Je mehr du löst, desto höher die Stufe. Später kommen Minus- und Kommazahlen dazu."],
      ["★", "Ränge durch Rechnen", "Dein Rang steigt mit jeder neuen Stufe. Dafür zählen nur richtig gelöste Aufgaben."],
    ]),
  },
];

let infoNummer = 0;
let infoTimer = null;

function infotafelZeigen(nummer) {
  infoNummer = (nummer + INFO_INHALTE.length) % INFO_INHALTE.length;
  const eintrag = INFO_INHALTE[infoNummer];
  document.getElementById("infotafel-titel").textContent = eintrag.titel;
  document.getElementById("infotafel-inhalt").innerHTML = eintrag.html;
  document.querySelectorAll("#infotafel-punkte button").forEach((punkt, i) => {
    punkt.classList.toggle("aktiv", i === infoNummer);
    punkt.setAttribute("aria-current", i === infoNummer ? "true" : "false");
  });
  // Timer neu starten, damit nach einem Klick nicht sofort weitergeblättert wird
  clearInterval(infoTimer);
  if (INFO_INHALTE.length > 1) {
    infoTimer = setInterval(() => infotafelZeigen(infoNummer + 1), INFO_WECHSEL_SEKUNDEN * 1000);
  }
}

function punktHinzufuegen(eintrag, i) {
  const punkt = document.createElement("button");
  punkt.type = "button";
  punkt.setAttribute("aria-label", eintrag.titel);
  punkt.addEventListener("click", () => infotafelZeigen(i));
  document.getElementById("infotafel-punkte").appendChild(punkt);
}

// Weiteren Eintrag anhängen und sofort zeigen (einmal pro Titel).
// Wird vom Easteregg genutzt: {titel, text} mit reinem Text, kein HTML.
function infotafelErgaenzen({ titel, text }) {
  if (INFO_INHALTE.some((eintrag) => eintrag.titel === titel)) return;
  const absatz = document.createElement("p");
  absatz.className = "erleuchtung-text";
  absatz.textContent = text;
  INFO_INHALTE.push({ titel, html: absatz.outerHTML });
  punktHinzufuegen(INFO_INHALTE[INFO_INHALTE.length - 1], INFO_INHALTE.length - 1);
  infotafelZeigen(INFO_INHALTE.length - 1);
}

(function infotafelAufbauen() {
  INFO_INHALTE.forEach(punktHinzufuegen);
  infotafelZeigen(0);
})();
