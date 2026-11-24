"""Registrieren, Anmelden und Passwörter (nur als Hash gespeichert)."""

import hashlib
import hmac
import secrets

import einstellungen
from app.datenbank.spieler_repository import SpielerRepository
from app.logik.spieler import Spieler

HASH_DURCHLAEUFE = 200_000


class AnmeldeFehler(Exception):
    """Fehler mit einer Meldung, die direkt im Browser angezeigt werden kann."""


class PasswortHasher:
    @staticmethod
    def hashen(passwort: str) -> str:
        salz = secrets.token_hex(16)
        wert = hashlib.pbkdf2_hmac("sha256", passwort.encode(), bytes.fromhex(salz), HASH_DURCHLAEUFE)
        return f"{salz}${wert.hex()}"

    @staticmethod
    def pruefen(passwort: str, gespeichert: str) -> bool:
        salz, wert = gespeichert.split("$", 1)
        neu = hashlib.pbkdf2_hmac("sha256", passwort.encode(), bytes.fromhex(salz), HASH_DURCHLAEUFE)
        return hmac.compare_digest(neu.hex(), wert)


class Benutzerverwaltung:
    def __init__(self, repository: SpielerRepository):
        self.repository = repository

    @staticmethod
    def passwort_regel_text() -> str:
        return (
            f"mindestens {einstellungen.PASSWORT_MIN_LAENGE} Zeichen, davon mindestens "
            f"{einstellungen.PASSWORT_MIN_SONDERZEICHEN} Sonderzeichen"
        )

    @staticmethod
    def passwort_gueltig(passwort: str) -> bool:
        sonderzeichen = sum(1 for zeichen in passwort if not zeichen.isalnum())
        return (
            len(passwort) >= einstellungen.PASSWORT_MIN_LAENGE
            and sonderzeichen >= einstellungen.PASSWORT_MIN_SONDERZEICHEN
        )

    def registrieren(self, benutzername: str, passwort: str, passwort_bestaetigen: str) -> Spieler:
        benutzername = benutzername.strip()
        if not benutzername:
            raise AnmeldeFehler("Bitte einen Benutzernamen eingeben.")
        if passwort != passwort_bestaetigen:
            raise AnmeldeFehler("Die Passwörter stimmen nicht überein.")
        if not self.passwort_gueltig(passwort):
            raise AnmeldeFehler(f"Das Passwort braucht {self.passwort_regel_text()}.")
        if self.repository.laden(benutzername) is not None:
            raise AnmeldeFehler("Diesen Benutzernamen gibt es schon.")
        spieler = Spieler(benutzername=benutzername, passwort_hash=PasswortHasher.hashen(passwort))
        self.repository.neu_anlegen(spieler)
        return spieler

    def anmelden(self, benutzername: str, passwort: str) -> Spieler:
        spieler = self.repository.laden(benutzername.strip())
        if spieler is None or not PasswortHasher.pruefen(passwort, spieler.passwort_hash):
            raise AnmeldeFehler("Benutzername oder Passwort ist falsch.")
        return spieler
