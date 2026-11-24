// Cookie-Klickseite.
// Klicks werden hier gesammelt und gebündelt an den Server geschickt.
// Gerechnet und geprüft wird nur auf dem Server, der Browser zeigt nur an.

let stand = null;          // letzter Spielstand vom Server
let offeneKlicks = [];     // Zeitstempel der noch nicht gemeldeten Klicks
let sendetGerade = false;

const el = (id) => document.getElementById(id);

function anzeigen() {
  if (!stand) return;
  // Angezeigte Cookies enthalten auch die noch nicht gesendeten Klicks
  const cookiesAnzeige = stand.cookies + offeneKlicks.length * stand.cookies_pro_klick;
  el("cookies").textContent = zahlFormat(cookiesAnzeige);
  el("pro-klick").textContent = zahlFormat(stand.cookies_pro_klick);

  // Rang = Name der aktuellen Stufe. Der Balken zählt die richtig gelösten
  // Aufgaben von 0 bis zur Schwelle des nächsten Rangs.
  el("rang").textContent = stand.rang;
  const prozent = stand.naechster_rang_ab
    ? Math.min(100, Math.max(0, stand.geloeste_aufgaben / stand.naechster_rang_ab * 100))
    : 100;
  el("rang-balken").style.width = prozent + "%";
  el("rang-balken").parentElement.setAttribute("aria-valuenow", Math.round(prozent));
  el("naechster-rang").textContent = stand.naechster_rang
    ? `Nächster Rang: ${stand.naechster_rang} ab ${zahlFormat(stand.naechster_rang_ab)} gelösten Aufgaben`
    : "Höchster Rang erreicht!";

  // Aufgabenkarte (der Zuwachs kommt immer vom Server, nie im Browser nachrechnen)
  document.querySelectorAll(".naechster-zuwachs").forEach((feld) => {
    feld.textContent = zahlFormat(stand.naechster_zuwachs);
  });
  el("preis").textContent = zahlFormat(stand.preis);
  el("stufe").textContent = stand.stufe;
  el("geloest").textContent = stand.geloeste_aufgaben;

  const aufgabeOffen = stand.offene_aufgabe !== null;
  el("ansicht-kaufen").classList.toggle("versteckt", aufgabeOffen);
  el("ansicht-aufgabe").classList.toggle("versteckt", !aufgabeOffen);
  if (aufgabeOffen) el("aufgabe-text").textContent = stand.offene_aufgabe;
  el("kaufen").disabled = aufgabeOffen || cookiesAnzeige < stand.preis;

  // Easteregg: Wer den Code gefunden hat, bekommt einen goldenen Cookie.
  document.body.classList.toggle("golden", stand.erleuchtet);

  // Easteregg: Beim höchsten Rang schickt der Server einen Hinweis für die Infotafel mit.
  if (stand.erleuchtung_hinweis) {
    infotafelErgaenzen({ titel: "Die Zahl der Erleuchtung", text: stand.erleuchtung_hinweis });
  }
}

function feedback(text, art) {
  const f = el("feedback");
  f.textContent = text;
  f.className = art || "";
}

// ---------------------------------------------------------------- Klicken

function klicken(x, y) {
  offeneKlicks.push(performance.timeOrigin + performance.now());
  plusAnzeigen(x, y);
  anzeigen();
}

el("cookie").addEventListener("pointerdown", (ereignis) => {
  el("cookie").classList.add("gedrueckt");
  klicken(ereignis.clientX, ereignis.clientY);
  zifferMerken(ereignis.clientX, ereignis.clientY);   // Easteregg, siehe unten
});
el("cookie").addEventListener("pointerup", () => el("cookie").classList.remove("gedrueckt"));
el("cookie").addEventListener("pointerleave", () => el("cookie").classList.remove("gedrueckt"));
el("cookie").addEventListener("keydown", (ereignis) => {
  if (ereignis.key !== "Enter" && ereignis.key !== " ") return;
  ereignis.preventDefault();
  if (ereignis.repeat) return;
  const rahmen = el("cookie").getBoundingClientRect();
  klicken(rahmen.left + rahmen.width / 2, rahmen.top + rahmen.height / 3);
});

function plusAnzeigen(x, y) {
  const bereich = el("cookie-bereich");
  const rahmen = bereich.getBoundingClientRect();
  const plus = document.createElement("span");
  plus.className = "plus";
  plus.textContent = "+" + zahlFormat(stand ? stand.cookies_pro_klick : 1);
  plus.style.left = x - rahmen.left + "px";
  plus.style.top = y - rahmen.top + "px";
  bereich.appendChild(plus);
  setTimeout(() => plus.remove(), 800);
}

// ---------------------------------------------------------------- Easteregg
// Auf dem Cookie stehen Ziffern. Jeder Klick zählt ganz normal als Cookie-Klick.
// Zusätzlich merken wir uns, welche Ziffer getroffen wurde, und fragen den Server,
// ob die Ziffern den geheimen Code ergeben. Den Code kennt nur der Server.
// Ein Klick auf eine Stelle ohne Ziffer fängt die Eingabe von vorne an.

let gedrueckteZiffern = "";

function zifferAnStelle(x, y) {
  // Alle Zahlen und Rechenzeichen auf dem Cookie-Bild durchgehen und die finden,
  // deren Rechteck die Klickstelle enthält.
  for (const zeichen of el("cookie").querySelectorAll("text")) {
    const r = zeichen.getBoundingClientRect();
    if (x >= r.left && x <= r.right && y >= r.top && y <= r.bottom) {
      const inhalt = zeichen.textContent.trim();
      return /^[0-9]$/.test(inhalt) ? inhalt : null;   // + und − sind keine Ziffern
    }
  }
  return null;
}

async function zifferMerken(x, y) {
  const ziffer = zifferAnStelle(x, y);
  if (ziffer === null) {
    gedrueckteZiffern = "";
    return;
  }
  gedrueckteZiffern = (gedrueckteZiffern + ziffer).slice(-10);  // nur die letzten 10 merken
  try {
    const antwort = await anfrage("/api/spiel/erleuchtung", { ziffern: gedrueckteZiffern });
    if (antwort.gefunden) {
      gedrueckteZiffern = "";
      stand.erleuchtet = true;   // ab jetzt goldener Cookie (der Server hat es gespeichert)
      anzeigen();
      el("erleuchtung-fenster").showModal();
    }
  } catch (fehler) {
    // Easteregg ist nicht wichtig genug für eine Fehlermeldung
  }
}

// Fenster schließen: mit "Weiter", dem X oder der Esc-Taste (macht der Browser selbst)
el("erleuchtung-weiter").addEventListener("click", () => el("erleuchtung-fenster").close());
el("erleuchtung-schliessen").addEventListener("click", () => el("erleuchtung-fenster").close());

// ---------------------------------------------------------------- Speichern

async function klicksSenden() {
  if (sendetGerade || offeneKlicks.length === 0) return;
  sendetGerade = true;
  const paket = offeneKlicks;
  offeneKlicks = [];
  try {
    stand = await anfrage("/api/spiel/klicks", { zeitstempel: paket });
    if (!stand.angenommen) {
      feedback("Klicks nicht gezählt: " + stand.grund, "falsch");
    }
  } catch (fehler) {
    offeneKlicks = paket.concat(offeneKlicks);  // beim nächsten Mal nochmal versuchen
  } finally {
    sendetGerade = false;
    anzeigen();
  }
}

// Beim Verlassen der Seite die letzten Klicks noch schnell mitschicken.
window.addEventListener("pagehide", () => {
  if (offeneKlicks.length === 0) return;
  const daten = new Blob([JSON.stringify({ zeitstempel: offeneKlicks })], { type: "application/json" });
  navigator.sendBeacon("/api/spiel/klicks", daten);
  offeneKlicks = [];
});

// ---------------------------------------------------------------- Aufgaben

el("kaufen").addEventListener("click", async () => {
  feedback("");
  await klicksSenden();
  try {
    stand = await anfrage("/api/spiel/kaufen", {});
    anzeigen();
    el("antwort").value = "";
    el("antwort").focus();
  } catch (fehler) {
    feedback(fehler.message, "falsch");
  }
});

el("antwort-form").addEventListener("submit", async (ereignis) => {
  ereignis.preventDefault();
  await klicksSenden();
  try {
    stand = await anfrage("/api/spiel/antworten", { antwort: el("antwort").value });
    if (stand.richtig) {
      feedback(`Richtig! +${zahlFormat(stand.zuwachs)} Cookies pro Klick`, "richtig");
    } else {
      feedback("Falsch!", "falsch");
    }
    anzeigen();
  } catch (fehler) {
    feedback(fehler.message, "falsch");
  }
});

el("zurueck").addEventListener("click", async () => {
  await klicksSenden();
  window.location.href = "/hauptmenue";
});

// ---------------------------------------------------------------- Start

anfrage("/api/spiel/stand").then((daten) => {
  stand = daten;
  anzeigen();
  setInterval(klicksSenden, stand.speicher_intervall_sekunden * 1000);
});
