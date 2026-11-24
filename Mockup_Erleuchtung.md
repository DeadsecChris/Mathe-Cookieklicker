# Mathecookie – Easteregg „Cookie der Erleuchtung“ als Overlay

Mockup: Canvas „Mathecookie Mockups“, Artboard **„Easteregg: Cookie der Erleuchtung“**.
Dieses Dokument ersetzt die Platzhalterseite `static/erleuchtung.html`.

## 1. Was sich ändert

Bisher führt der richtige Code (`ERLEUCHTUNGS_CODE`) auf eine **eigene Seite** `/erleuchtung`.
Neu ist ein **Fenster über der Klickseite**. Die Klickseite bleibt dahinter gedämpft und leicht verschwommen sichtbar, und der Spieler bleibt auf `/spiel`.

Die Erkennung des Codes bleibt, wie sie ist: Ziffern auf dem Cookie, `Erleuchtung.code_passt()`, Hinweis in der Infotafel ab dem höchsten Rang. Geprüft wird weiter nur auf dem Server.

## 2. Backend

- `POST /api/spiel/erleuchtung` (`app/routen/spiel.py`) gibt statt `{"geheimseite": "/erleuchtung"}` jetzt `{"erleuchtet": true}` zurück, bei falschem Code `{"erleuchtet": false}`.
- Danach werden nicht mehr gebraucht und können weg: `GET /erleuchtung` in `app/routen/seiten.py`, `erleuchten()`, `ist_erleuchtet()` und `_erleuchtet` in `app/sitzungen.py` sowie `static/erleuchtung.html`. Die passenden Tests anpassen.
- `einstellungen.py`, `app/logik/erleuchtung.py` und der Infotafel-Hinweis bleiben unverändert.

## 3. Frontend

### 3.1 `spiel.js`

In `zifferMerken()`:
```js
const antwort = await anfrage("/api/spiel/erleuchtung", { ziffern: gedrueckteZiffern });
if (antwort.erleuchtet) {
  gedrueckteZiffern = "";
  document.getElementById("erleuchtung").showModal();
}
```
`klicksSenden()` und den Seitenwechsel braucht es hier nicht mehr, weil die Seite offen bleibt.
Schließen per X-Knopf, per „Weiter“-Knopf und per Esc (macht `<dialog>` selbst) mit `dialog.close()`. Danach geht das Spiel normal weiter.

### 3.2 `spiel.html`: neues `<dialog id="erleuchtung" aria-labelledby="erleuchtung-titel">`

Von oben nach unten:
1. **X-Knopf** oben rechts: rund, 44px, `aria-label="Schließen"`, `border: 2px solid #E0B040`, Icon `#FFE9A8`.
2. **„Glückwunsch!“** (`#erleuchtung-titel`): Fredoka 44px, `#FFD966`, `text-shadow: 0 0 18px rgba(255,214,90,.6)`.
3. **Goldener Cookie mit heiliger Aura**, Bereich ca. 420 × 400px, Cookie ca. 260px. Ebenen von hinten nach vorn:
   - **Goldene Strahlen**: Kreisfläche 560px, `repeating-conic-gradient(from 0deg, rgba(255,222,120,.55) 0deg 5deg, rgba(255,222,120,0) 5deg 15deg)`, nach außen ausgeblendet mit `mask-image: radial-gradient(circle, #000 20%, transparent 65%)`. Dreht sich langsam: `animation: drehen 40s linear infinite`.
   - **Heller Schein**: Kreis 380px, `radial-gradient(circle, rgba(255,246,200,.95) 0%, rgba(255,214,90,.6) 35%, rgba(255,190,40,0) 70%)`. Pulsiert: Deckkraft .85 → 1 und Größe 1 → 1.06, 3 s.
   - **Heiligenschein**: Ellipse 170 × 40px über dem Cookie, `border: 7px solid #FFE27A`, `box-shadow: 0 0 18px #FFD54A, inset 0 0 12px #FFD54A`. Pulsiert mit.
   - **Goldener Cookie**: neue Datei `static/bilder/goldcookie.svg` (Anhang). Leuchtet mit `filter: drop-shadow(0 0 22px rgba(255,214,90,.9))`. `alt="Goldener Cookie der Erleuchtung"`.
   - **5 Funkelsterne**: vierzackig, `#FFF3B0`, 18–36px, um den Cookie verteilt. Blinken versetzt (2,4 s, Deckkraft .25 → 1, Größe .7 → 1).
4. **„Dies ist der Cookie der Erleuchtung!“**: Fredoka 30px, `#FFE9A8`.
5. **„Ab sofort bist du damit gesegnet!“**: Nunito 20px fett, `#FFEFD6`.
6. **Knopf „Weiter“**: Hintergrund `#F5C542`, Text `#3A1C08`, Fredoka 20px, mind. 52px hoch, `box-shadow: 0 4px 0 #A87A12, 0 0 24px rgba(255,214,90,.45)`. Schließt das Fenster.

### 3.3 `stil.css`

```css
#erleuchtung {
  width: min(640px, calc(100% - 32px));
  margin: 110px auto auto;              /* oben mit Abstand, Klickseite unten sichtbar */
  padding: 28px 32px 36px;
  background: #3A1C08;
  border: 6px solid #E0B040;
  outline: 2px solid #7A5410;
  border-radius: 32px;
  box-shadow: 0 0 0 10px rgba(224,176,64,.15), 0 0 80px rgba(255,214,90,.45), 0 30px 60px rgba(0,0,0,.5);
  text-align: center;
  overflow: hidden;
  color: #FFEFD6;
}
#erleuchtung::backdrop {
  background: rgba(36,16,4,.62);
  backdrop-filter: blur(3px);
}
@keyframes drehen  { to { transform: rotate(360deg); } }
@keyframes puls    { 0%,100% { opacity:.85; transform:scale(1); } 50% { opacity:1; transform:scale(1.06); } }
@keyframes funkeln { 0%,100% { opacity:.25; transform:scale(.7); } 50% { opacity:1; transform:scale(1); } }
@media (prefers-reduced-motion: reduce) {
  #erleuchtung * { animation: none !important; }
}
```

## 4. Offen

- Was bewirkt „Ab sofort bist du damit gesegnet!“ im Spiel? Bleibt es nur ein Text, oder ist es ein dauerhafter Effekt (z. B. ein Bonus)? Falls dauerhaft, braucht `Spieler` ein gespeichertes Feld (z. B. `gesegnet: bool`), das im Spielstand mitkommt, und die Werte gehören nach `einstellungen.py`.
- Erscheint das Fenster bei jeder richtigen Eingabe des Codes oder nur beim ersten Mal?

## Anhang – `static/bilder/goldcookie.svg`

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <defs>
    <radialGradient id="gold" cx="38%" cy="32%" r="75%">
      <stop offset="0%" stop-color="#FFF6C4"/>
      <stop offset="45%" stop-color="#F7CB4A"/>
      <stop offset="85%" stop-color="#D49A1C"/>
      <stop offset="100%" stop-color="#A8760E"/>
    </radialGradient>
  </defs>
  <path d="M100 8 C150 6 192 44 192 98 C194 150 152 192 100 192 C46 194 8 152 8 100 C6 50 48 10 100 8 Z" fill="url(#gold)" stroke="#8A6212" stroke-width="4"/>
  <g fill="#9C6C10">
    <ellipse cx="62" cy="58" rx="11" ry="9" transform="rotate(-20 62 58)"/>
    <ellipse cx="122" cy="46" rx="9" ry="8"/>
    <ellipse cx="150" cy="96" rx="12" ry="9" transform="rotate(30 150 96)"/>
    <ellipse cx="96" cy="98" rx="10" ry="9"/>
    <ellipse cx="50" cy="120" rx="10" ry="8" transform="rotate(15 50 120)"/>
    <ellipse cx="108" cy="148" rx="12" ry="9" transform="rotate(-25 108 148)"/>
    <ellipse cx="152" cy="150" rx="8" ry="7"/>
    <ellipse cx="74" cy="160" rx="7" ry="6"/>
  </g>
  <g fill="#FFFBE0" opacity="0.8">
    <circle cx="70" cy="44" r="4"/><circle cx="84" cy="70" r="3"/><circle cx="138" cy="70" r="2.5"/>
    <circle cx="128" cy="124" r="3"/><circle cx="40" cy="90" r="2.5"/>
  </g>
</svg>
```
