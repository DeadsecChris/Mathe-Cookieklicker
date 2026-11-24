"""
Mathecookie starten.

    python start.py

Startet nur, richtet nichts ein (Konvention im Unibrain):
  1. prüft, ob einrichten.py schon gelaufen ist
  2. startet die lokale MongoDB, falls sie noch nicht läuft
  3. startet den Webserver (FastAPI)
  4. öffnet die Anmeldeseite im Browser

Beenden: Strg+C in diesem Fenster.
"""

import glob
import os
import shutil
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

import einstellungen

ORDNER = Path(__file__).resolve().parent
VENV = ORDNER / ".venv"
MONGO_DATEN = ORDNER / "daten" / "mongodb"


def venv_python() -> Path:
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def abbrechen(grund: str):
    print(f"\nFEHLER: {grund}")
    input("\nEnter zum Schließen ...")
    sys.exit(1)


def port_offen(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def warten_auf_port(host: str, port: int, sekunden: float) -> bool:
    ende = time.time() + sekunden
    while time.time() < ende:
        if port_offen(host, port):
            return True
        time.sleep(0.3)
    return False


def mongod_finden():
    gefunden = shutil.which("mongod")
    if gefunden:
        return gefunden
    if os.name == "nt":
        treffer = sorted(glob.glob(r"C:\Program Files\MongoDB\Server\*\bin\mongod.exe"))
        if treffer:
            return treffer[-1]
    return None


def pruefe_einrichtung():
    if not venv_python().exists():
        abbrechen("Die virtuelle Umgebung .venv fehlt. Bitte zuerst ausführen:  python einrichten.py")
    test = subprocess.run(
        [str(venv_python()), "-c", "import fastapi, uvicorn, pymongo"],
        capture_output=True,
    )
    if test.returncode != 0:
        abbrechen("Es fehlen Pakete in .venv. Bitte ausführen:  python einrichten.py")


def mongodb_starten():
    """Gibt den gestarteten Prozess zurück (oder None, wenn MongoDB schon lief)."""
    host, port = einstellungen.MONGO_HOST, einstellungen.MONGO_PORT
    if port_offen(host, port):
        print(f"MongoDB läuft bereits ({host}:{port}).")
        return None

    # 1. Versuch: Windows-Dienst "MongoDB" (Standard bei der Installation)
    if os.name == "nt":
        print("Starte Windows-Dienst MongoDB ...")
        subprocess.run(["net", "start", "MongoDB"], capture_output=True)
        if warten_auf_port(host, port, 10):
            print("MongoDB-Dienst läuft.")
            return None

    # 2. Versuch: mongod direkt starten, mit Datenordner im Projekt
    mongod = mongod_finden()
    if mongod is None:
        abbrechen(
            "MongoDB läuft nicht und mongod wurde nicht gefunden.\n"
            "Bitte MongoDB Community Server installieren (siehe README.md) und danach  python einrichten.py"
        )
    if not MONGO_DATEN.exists():
        abbrechen("Der Ordner daten/mongodb fehlt. Bitte zuerst ausführen:  python einrichten.py")

    print(f"Starte MongoDB: {mongod}")
    prozess = subprocess.Popen(
        [mongod, "--dbpath", str(MONGO_DATEN), "--port", str(port), "--bind_ip", "127.0.0.1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if not warten_auf_port(host, port, 20):
        prozess.terminate()
        abbrechen("MongoDB ließ sich nicht starten. Läuft vielleicht schon eine andere Instanz?")
    print("MongoDB läuft.")
    return prozess


def server_starten():
    host, port = einstellungen.SERVER_HOST, einstellungen.SERVER_PORT
    if port_offen(host, port):
        abbrechen(f"Port {port} ist schon belegt. Läuft Mathecookie schon in einem anderen Fenster?")
    print("Starte Webserver ...")
    prozess = subprocess.Popen(
        [str(venv_python()), "-m", "uvicorn", "app.main:erstelle_app", "--factory",
         "--host", host, "--port", str(port)],
        cwd=str(ORDNER),
    )
    if not warten_auf_port(host, port, 20):
        prozess.terminate()
        abbrechen("Der Webserver ist nicht gestartet. Die Fehlermeldung steht oben.")
    return prozess


def main():
    print("=== Mathecookie ===")
    pruefe_einrichtung()
    mongo = mongodb_starten()
    server = server_starten()

    adresse = f"http://{einstellungen.SERVER_HOST}:{einstellungen.SERVER_PORT}/"
    print(f"\nMathecookie läuft: {adresse}")
    print("Beenden mit Strg+C.\n")
    webbrowser.open(adresse)

    try:
        server.wait()
    except KeyboardInterrupt:
        print("\nBeende Mathecookie ...")
    finally:
        server.terminate()
        if mongo is not None:
            mongo.terminate()


if __name__ == "__main__":
    main()
