# Mathecookie

Cookie-Clicker mit Matheaufgaben (Schul-Miniprojekt Programmieren).
Klick auf den Cookie, kauf dir Rechenaufgaben und bekomm für richtige Antworten mehr Cookies pro Klick.

Spiellogik und Entscheidungen: `Obsidian_Vault/Schule/Programmieren/Programmieren_Miniprojekt/Spiellogik.md` im Unibrain.

## Schnellstart für neue Spieler

1. **Python installieren** (3.10 oder neuer): https://www.python.org/downloads/
   Unter Windows beim Installieren den Haken bei „Add Python to PATH“ setzen.
2. **MongoDB installieren**: „MongoDB Community Server“ von https://www.mongodb.com/try/download/community
   Bei der Installation „Install MongoD as a Service“ angehakt lassen, dann läuft die Datenbank automatisch.
3. **Projekt herunterladen**: oben auf GitHub „Code“ → „Download ZIP“ und entpacken
   (oder `git clone https://github.com/DeadsecChris/Mathe-Cookieklicker.git`).
4. **Ordner in VS Code öffnen** (Datei → Ordner öffnen) und im Terminal einmalig ausführen:
   ```
   python einrichten.py
   ```
   Am Ende sollte „MongoDB gefunden“ stehen. Wenn nicht, Schritt 2 prüfen.
5. **Spiel starten**:
   ```
   python start.py
   ```
   Der Browser öffnet sich mit http://127.0.0.1:8000. Dort ein Konto registrieren und losklicken.
   Beenden mit Strg+C im Terminal.

Ohne VS Code geht es genauso in einer Eingabeaufforderung, die im Projektordner geöffnet ist.

## Voraussetzungen

- Python 3.10 oder neuer
- MongoDB Community Server (lokal), z. B. als Windows-Dienst „MongoDB“

## Einrichten (einmalig)

```
python einrichten.py
```

Legt `.venv` an, installiert die Pakete aus `requirements.txt` und den Ordner `daten/mongodb`.

## Starten

```
python start.py
```

Startet MongoDB (falls sie nicht schon läuft), den Webserver und öffnet http://127.0.0.1:8000 im Browser.
Beenden mit Strg+C.

## Werte anpassen

Alle Spielwerte (Preise, Zuwachs, Stufen, Ränge, Passwort-Regel, Klickschutz) stehen in **`einstellungen.py`**.
Wert ändern, speichern, `start.py` neu starten.

## Aufbau

```
start.py                  startet alles (richtet nichts ein)
einrichten.py             einmalige Einrichtung
einstellungen.py          alle einstellbaren Werte
app/
  main.py                 FastAPI-App, baut alles zusammen
  sitzungen.py            wer ist angemeldet
  abhaengigkeiten.py      angemeldeten Spieler für die Routen laden
  routen/                 dünne Routen: seiten.py, konto.py, spiel.py
  logik/                  Spiellogik in Klassen
    spieler.py            Spielstand (Klasse Spieler)
    rechenaufgabe.py      eine Aufgabe, Antwort prüfen
    schwierigkeitsgrad.py Stufen
    aufgaben_generator.py zufällige Aufgaben je Stufe
    shop.py               Kaufpreis
    rang_system.py        Ränge (bleiben, wenn einmal erreicht)
    erleuchtung.py        Easteregg: Zahl der Erleuchtung
    klick_pruefer.py      Schutz gegen Auto-Klicker
    benutzerverwaltung.py Registrieren, Anmelden, Passwort-Hash
    spiel.py              Spielablauf (verbindet alles)
  datenbank/
    spieler_repository.py MongoDB-Zugriff
static/                   HTML, CSS, JavaScript, Cookie-Bild
tests/                    python -m unittest
```
