// Kleine Hilfsfunktion für Anfragen an den Server (JSON hin und zurück).
async function anfrage(pfad, daten) {
  const optionen = { method: daten === undefined ? "GET" : "POST", headers: {} };
  if (daten !== undefined) {
    optionen.headers["Content-Type"] = "application/json";
    optionen.body = JSON.stringify(daten);
  }
  const antwort = await fetch(pfad, optionen);
  if (antwort.status === 401) {
    window.location.href = "/";
    throw new Error("Nicht angemeldet.");
  }
  const inhalt = await antwort.json();
  if (!antwort.ok) {
    throw new Error(inhalt.detail || "Unbekannter Fehler.");
  }
  return inhalt;
}

function zahlFormat(zahl) {
  return Number(zahl).toLocaleString("de-DE");
}
