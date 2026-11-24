"""
==========================================================================
  MATHECOOKIE – EINSTELLUNGEN
==========================================================================

Hier stehen ALLE Spielwerte an einer Stelle. Zum Testen einfach einen
Wert ändern, speichern und das Programm neu starten (start.py).

Die Klassen im Ordner app/ lesen ihre Werte nur aus dieser Datei.
Es gibt keine "versteckten" Zahlen im restlichen Code.
"""

# --------------------------------------------------------------------------
#  1. COOKIES PRO KLICK
# --------------------------------------------------------------------------

# Cookies pro Klick bei einem neuen oder zurückgesetzten Spielstand.
START_COOKIES_PRO_KLICK = 1

# Nach jeder RICHTIG gelösten Aufgabe werden die Cookies pro Klick damit
# multipliziert (und gerundet), genau wie beim PREISFAKTOR.
# Es gibt aber immer mindestens +1 Cookie pro Klick.
# Beispiel mit 1.4: 1 -> 2 -> 3 -> 4 (statt 4,5 gerundet) -> 6 -> 9 -> 14 ...
ZUWACHS_FAKTOR = 1.4


# --------------------------------------------------------------------------
#  2. KAUFPREIS DER RECHENAUFGABEN
# --------------------------------------------------------------------------

# Preis der allerersten Rechenaufgabe.
STARTPREIS = 20

# Nach jeder RICHTIG gelösten Aufgabe wird der Preis damit multipliziert
# (und gerundet). Bei einer falschen Antwort bleibt der Preis gleich.
# Preis = STARTPREIS × PREISFAKTOR ^ (Anzahl richtig gelöster Aufgaben)
PREISFAKTOR = 1.5


# --------------------------------------------------------------------------
#  3. SCHWIERIGKEITSGRADE (STUFEN)
# --------------------------------------------------------------------------
#
#  ab_geloest     : ab so vielen RICHTIG gelösten Aufgaben gilt diese Stufe
#  zahlen_von/bis : Bereich der Zufallszahlen (beide Grenzen inklusive)
#  operationen    : erlaubte Rechenzeichen: "+", "-", "*", "/"
#                   Geteilt-Aufgaben gehen IMMER glatt auf (keine Kommazahlen).
#  anzahl_zahlen  : wie viele Zahlen in einer Aufgabe vorkommen
#  rang           : Rangname, den man mit dieser Stufe erreicht (siehe Abschnitt 4)
#
#  Die Stufen müssen nach ab_geloest aufsteigend sortiert sein.
#  Die erste Stufe muss ab_geloest = 0 haben.

STUFEN = [
    {"ab_geloest": 0,  "zahlen_von": 1, "zahlen_bis": 10,       "operationen": ["+"],                "anzahl_zahlen": 2, "rang": "Lehrling"},  # Stufe 1
    {"ab_geloest": 5,  "zahlen_von": 1, "zahlen_bis": 50,       "operationen": ["+", "-"],           "anzahl_zahlen": 2, "rang": "Krümelmonster"},  # Stufe 2
    {"ab_geloest": 10, "zahlen_von": 1, "zahlen_bis": 10,       "operationen": ["*"],                "anzahl_zahlen": 2, "rang": "Cookie-Schubser"},  # Stufe 3
    {"ab_geloest": 20, "zahlen_von": 1, "zahlen_bis": 20,       "operationen": ["*", "/"],           "anzahl_zahlen": 2, "rang": "Cookie-Gelehrter"},  # Stufe 4
    {"ab_geloest": 30, "zahlen_von": -100, "zahlen_bis": 100,   "operationen": ["+", "-", "*"],      "anzahl_zahlen": 2, "rang": "Halbprofi"},  # Stufe 5
    {"ab_geloest": 40, "zahlen_von": -100, "zahlen_bis": 200,   "operationen": ["+", "-", "*", "/"], "anzahl_zahlen": 2, "rang": "Vollprofi"},  # Stufe 6
    {"ab_geloest": 60, "zahlen_von": -100, "zahlen_bis": 200,   "operationen": ["+", "-", "*", "/"], "anzahl_zahlen": 3, "rang": "Cookie-Meister"},  # Stufe 7
    {"ab_geloest": 80, "zahlen_von": -100, "zahlen_bis": 1000,  "operationen": ["+", "-", "*", "/"], "anzahl_zahlen": 3, "rang": "Cookie-Großmeister"},  # Stufe 8
    {"ab_geloest": 100, "zahlen_von": -100, "zahlen_bis": 1000, "operationen": ["+", "-", "*", "/"], "anzahl_zahlen": 4, "rang": "Cookie-König"},  # Stufe 9
    {"ab_geloest": 120, "zahlen_von": -100, "zahlen_bis": 1000, "operationen": ["+", "-", "*", "/"], "anzahl_zahlen": 4, "rang": "Erleuchteter Cookie-Herrscher"},  # Stufe 10
]

# Ab dieser Stufe dürfen Ergebnisse negativ sein (darunter nur >= 0).
NEGATIV_AB_STUFE = 4

# Ab dieser Stufe können Kommazahlen vorkommen, aber NUR in Aufgaben,
# die ausschließlich aus Plus und Minus bestehen (z. B. 12,5 + 3,7).
KOMMA_AB_STUFE = 4

# So viele Stellen nach dem Komma haben die Kommazahlen.
NACHKOMMASTELLEN = 1

# Anteil der Plus/Minus-Aufgaben (ab KOMMA_AB_STUFE), die mit Kommazahlen
# gestellt werden. 0.5 = etwa jede zweite, 1.0 = immer, 0 = nie.
KOMMA_ANTEIL = 0.5


# --------------------------------------------------------------------------
#  4. RÄNGE
# --------------------------------------------------------------------------
#
#  Der Rang ist der Name der aktuellen Stufe (Feld "rang" in STUFEN oben).
#  Man steigt also mit richtig gelösten Aufgaben auf, nicht mit Cookies.
#  Da gelöste Aufgaben nie weniger werden, sinkt der Rang nie
#  (außer beim Zurücksetzen des Spielstands).


# --------------------------------------------------------------------------
#  5. PASSWORT-REGELN
# --------------------------------------------------------------------------

# Mindestlänge des Passworts.
PASSWORT_MIN_LAENGE = 4

# So viele Sonderzeichen (weder Buchstabe noch Ziffer) muss es mindestens haben.
PASSWORT_MIN_SONDERZEICHEN = 1


# --------------------------------------------------------------------------
#  6. KLICKS SPEICHERN UND SCHUTZ GEGEN AUTO-KLICKER
# --------------------------------------------------------------------------

# So oft (in Sekunden) schickt der Browser die gesammelten Klicks an den Server.
SPEICHER_INTERVALL_SEKUNDEN = 5

# Mehr Klicks pro Sekunde werden nicht angenommen (das ganze Paket verfällt).
MAX_KLICKS_PRO_SEKUNDE = 20

# Ab so vielen Klicks in einem Paket wird der Klick-Rhythmus geprüft.
RHYTHMUS_MIN_KLICKS = 20

# Schwanken die Abstände zwischen den Klicks weniger als so viele
# Millisekunden (Standardabweichung), gilt das Paket als Auto-Klicker.
RHYTHMUS_MIN_STREUUNG_MS = 5


# --------------------------------------------------------------------------
#  7. TECHNIK (normalerweise nicht ändern)
# --------------------------------------------------------------------------

# Adresse und Port der Webanwendung (im Browser: http://127.0.0.1:8000).
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

# Lokale MongoDB.
MONGO_HOST = "localhost"
MONGO_PORT = 27017
DATENBANK_NAME = "mathecookie"


# --------------------------------------------------------------------------
#  8. EASTEREGG: DIE ZAHL DER ERLEUCHTUNG
# --------------------------------------------------------------------------
#
#  Auf dem Cookie der Klickseite stehen Ziffern. Drückt man sie in genau
#  dieser Reihenfolge, öffnet sich die geheime Glückwunschseite.
#  Ein Klick auf eine Stelle ohne Ziffer fängt die Eingabe von vorne an.
#  Es dürfen nur Ziffern vorkommen, die auch auf dem Cookie stehen (6 7 9 1 4 0).
#  Der Code steht nur hier auf dem Server, nie im JavaScript.

ERLEUCHTUNGS_CODE = "67911"

# Diesen Text zeigt die Infotafel unter dem Cookie, sobald man den
# höchsten Rang erreicht hat. {code} wird durch ERLEUCHTUNGS_CODE ersetzt.
ERLEUCHTUNGS_HINWEIS = (
    "Glückwunsch! Du bist nun der erleuchtete Cookieherrscher. "
    "Jetzt kannst du die wahre Gestalt des Cookies erkennen. "
    "Die Zahl der Erleuchtung ist {code}"
)
