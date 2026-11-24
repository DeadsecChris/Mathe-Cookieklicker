"""Spielstand eines Spielers."""

from dataclasses import dataclass, field
from typing import Optional

import einstellungen
from app.logik.rechenaufgabe import Rechenaufgabe


@dataclass
class Spieler:
    benutzername: str
    passwort_hash: str
    cookies: int = 0
    cookies_pro_klick: int = field(default_factory=lambda: einstellungen.START_COOKIES_PRO_KLICK)
    geloeste_aufgaben: int = 0
    offene_aufgabe: Optional[Rechenaufgabe] = None
    erleuchtet: bool = False   # Easteregg gefunden? Dann ist der Cookie golden.

    def klicks_gutschreiben(self, anzahl: int) -> int:
        dazu = anzahl * self.cookies_pro_klick
        self.cookies += dazu
        return dazu

    def bezahlen(self, preis: int) -> bool:
        if self.cookies < preis:
            return False
        self.cookies -= preis
        return True

    def aufgabe_beantwortet(self, richtig: bool, zuwachs: int):
        if richtig:
            self.geloeste_aufgaben += 1
            self.cookies_pro_klick += zuwachs
        self.offene_aufgabe = None

    def zuruecksetzen(self):
        self.cookies = 0
        self.cookies_pro_klick = einstellungen.START_COOKIES_PRO_KLICK
        self.geloeste_aufgaben = 0
        self.offene_aufgabe = None
        self.erleuchtet = False

    # Speichern in der Datenbank

    def als_dict(self) -> dict:
        return {
            "benutzername": self.benutzername,
            "passwort_hash": self.passwort_hash,
            "cookies": self.cookies,
            "cookies_pro_klick": self.cookies_pro_klick,
            "geloeste_aufgaben": self.geloeste_aufgaben,
            "offene_aufgabe": self.offene_aufgabe.als_dict() if self.offene_aufgabe else None,
            "erleuchtet": self.erleuchtet,
        }

    @classmethod
    def aus_dict(cls, daten: dict) -> "Spieler":
        offene = daten.get("offene_aufgabe")
        return cls(
            benutzername=daten["benutzername"],
            passwort_hash=daten["passwort_hash"],
            cookies=daten.get("cookies", 0),
            cookies_pro_klick=daten.get("cookies_pro_klick", einstellungen.START_COOKIES_PRO_KLICK),
            geloeste_aufgaben=daten.get("geloeste_aufgaben", 0),
            offene_aufgabe=Rechenaufgabe.aus_dict(offene) if offene else None,
            erleuchtet=daten.get("erleuchtet", False),   # ältere Spielstände haben das Feld noch nicht
        )
