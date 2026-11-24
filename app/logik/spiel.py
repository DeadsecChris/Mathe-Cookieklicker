"""Spielablauf: verbindet Spieler, Aufgaben, Shop, Ränge und Klickprüfung."""

import time
from typing import TYPE_CHECKING

import einstellungen
from app.logik.aufgaben_generator import AufgabenGenerator
from app.logik.erleuchtung import Erleuchtung
from app.logik.klick_pruefer import KlickPruefer
from app.logik.rang_system import RangSystem
from app.logik.shop import Shop
from app.logik.spieler import Spieler

if TYPE_CHECKING:  # nur für die Typangabe, so bleibt die Logik ohne Datenbank testbar
    from app.datenbank.spieler_repository import SpielerRepository


class SpielFehler(Exception):
    """Fehler mit einer Meldung für den Browser."""


class Spiel:
    def __init__(self, repository: "SpielerRepository"):
        self.repository = repository
        self.generator = AufgabenGenerator()
        self.shop = Shop()
        self.raenge = RangSystem(self.generator.stufenliste)
        self.klick_pruefer = KlickPruefer()
        self.erleuchtung = Erleuchtung(self.raenge)   # Easteregg
        self._letztes_paket = {}  # benutzername -> Zeitpunkt (Server-Uhr)

    # ------------------------------------------------------------------ Anzeige

    def spielstand(self, spieler: Spieler) -> dict:
        naechster = self.raenge.naechster(spieler.geloeste_aufgaben)
        return {
            "benutzername": spieler.benutzername,
            "cookies": spieler.cookies,
            "cookies_pro_klick": spieler.cookies_pro_klick,
            "rang": self.raenge.rang(spieler.geloeste_aufgaben),
            "naechster_rang": naechster[0] if naechster else None,
            "naechster_rang_ab": naechster[1] if naechster else None,   # gelöste Aufgaben
            "stufe": self.generator.stufenliste.stufe_fuer(spieler.geloeste_aufgaben).nummer,
            "geloeste_aufgaben": spieler.geloeste_aufgaben,
            "preis": self.shop.preis(spieler.geloeste_aufgaben),
            "naechster_zuwachs": self.zuwachs(spieler.cookies_pro_klick),
            "offene_aufgabe": spieler.offene_aufgabe.text if spieler.offene_aufgabe else None,
            "speicher_intervall_sekunden": einstellungen.SPEICHER_INTERVALL_SEKUNDEN,
            # Easteregg: golden, wenn freigeschaltet. Text mit dem Code nur beim höchsten Rang, sonst None
            "erleuchtet": spieler.erleuchtet,
            "erleuchtung_hinweis": self.erleuchtung.hinweis(spieler.geloeste_aufgaben),
        }

    # ------------------------------------------------------------------ Aktionen

    def klicks_melden(self, spieler: Spieler, zeitstempel_ms: list) -> dict:
        jetzt = time.monotonic()
        vorher = self._letztes_paket.get(spieler.benutzername)
        seit_letztem = (jetzt - vorher) if vorher is not None else None
        self._letztes_paket[spieler.benutzername] = jetzt

        ergebnis = self.klick_pruefer.pruefen(zeitstempel_ms, seit_letztem)
        if not ergebnis.gueltig:
            return {"angenommen": False, "grund": ergebnis.grund, **self.spielstand(spieler)}

        spieler.klicks_gutschreiben(len(zeitstempel_ms))
        self.repository.speichern(spieler)
        return {"angenommen": True, **self.spielstand(spieler)}

    def aufgabe_kaufen(self, spieler: Spieler) -> dict:
        if spieler.offene_aufgabe is not None:
            raise SpielFehler("Du hast schon eine offene Aufgabe. Erst beantworten!")
        # Der Preis steigt nur mit richtig gelösten Aufgaben, falsche Antworten machen nichts teurer.
        preis = self.shop.preis(spieler.geloeste_aufgaben)
        if not spieler.bezahlen(preis):
            raise SpielFehler(f"Du brauchst {preis} Cookies für die nächste Aufgabe.")
        spieler.offene_aufgabe = self.generator.neue_aufgabe(spieler.geloeste_aufgaben)
        self.repository.speichern(spieler)
        return self.spielstand(spieler)

    def aufgabe_beantworten(self, spieler: Spieler, antwort: str) -> dict:
        aufgabe = spieler.offene_aufgabe
        if aufgabe is None:
            raise SpielFehler("Es gibt keine offene Aufgabe. Kauf zuerst eine.")
        if aufgabe.eingabe_lesen(antwort) is None:
            raise SpielFehler("Bitte eine Zahl eingeben.")
        richtig = aufgabe.ist_richtig(antwort)
        zuwachs = self.zuwachs(spieler.cookies_pro_klick) if richtig else 0
        spieler.aufgabe_beantwortet(richtig, zuwachs)
        self.repository.speichern(spieler)
        return {"richtig": richtig, "zuwachs": zuwachs, **self.spielstand(spieler)}

    def erleuchtung_pruefen(self, spieler: Spieler, gedrueckte_ziffern: str) -> dict:
        """Easteregg: Ergeben die gedrückten Ziffern den Code, wird der Spieler erleuchtet
        (goldener Cookie, in der Datenbank gespeichert)."""
        gefunden = self.erleuchtung.code_passt(gedrueckte_ziffern)
        if gefunden and not spieler.erleuchtet:
            spieler.erleuchtet = True
            self.repository.speichern(spieler)
        return {"gefunden": gefunden, **self.spielstand(spieler)}

    @staticmethod
    def zuwachs(cookies_pro_klick: int) -> int:
        """Cookies pro Klick × ZUWACHS_FAKTOR (gerundet), mindestens +1."""
        neu = round(cookies_pro_klick * einstellungen.ZUWACHS_FAKTOR)
        return max(1, neu - cookies_pro_klick)

    def zuruecksetzen(self, spieler: Spieler) -> dict:
        spieler.zuruecksetzen()
        self.repository.speichern(spieler)
        return self.spielstand(spieler)
