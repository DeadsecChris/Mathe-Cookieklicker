"""
Mathecookie einrichten (einmalig bzw. nach Änderungen an requirements.txt).

    python einrichten.py

Macht:
  1. virtuelle Umgebung .venv anlegen (falls noch nicht da)
  2. Pakete aus requirements.txt installieren
  3. Ordner daten/mongodb für eine selbst gestartete MongoDB anlegen
  4. prüfen, ob MongoDB installiert ist (installiert sie aber NICHT)
"""

import glob
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ORDNER = Path(__file__).resolve().parent
VENV = ORDNER / ".venv"


def venv_python() -> Path:
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def mongod_finden():
    gefunden = shutil.which("mongod")
    if gefunden:
        return gefunden
    if os.name == "nt":
        treffer = sorted(glob.glob(r"C:\Program Files\MongoDB\Server\*\bin\mongod.exe"))
        if treffer:
            return treffer[-1]
    return None


def main():
    if sys.version_info < (3, 10):
        sys.exit("Mathecookie braucht Python 3.10 oder neuer.")

    if not venv_python().exists():
        print("1/4  Lege virtuelle Umgebung .venv an ...")
        venv.create(VENV, with_pip=True)
    else:
        print("1/4  Virtuelle Umgebung .venv ist schon da.")

    print("2/4  Installiere Pakete aus requirements.txt ...")
    subprocess.check_call([str(venv_python()), "-m", "pip", "install", "--upgrade", "pip", "-q"])
    subprocess.check_call([str(venv_python()), "-m", "pip", "install", "-r", str(ORDNER / "requirements.txt")])

    print("3/4  Lege Ordner daten/mongodb an ...")
    (ORDNER / "daten" / "mongodb").mkdir(parents=True, exist_ok=True)

    print("4/4  Prüfe MongoDB ...")
    mongod = mongod_finden()
    if mongod:
        print(f"     MongoDB gefunden: {mongod}")
    else:
        print("     MongoDB wurde nicht gefunden.")
        print("     Bitte 'MongoDB Community Server' installieren: https://www.mongodb.com/try/download/community")
        print("     (Wenn MongoDB als Windows-Dienst läuft, ist das auch in Ordnung.)")

    print("\nFertig. Starten mit:  python start.py")


if __name__ == "__main__":
    main()
