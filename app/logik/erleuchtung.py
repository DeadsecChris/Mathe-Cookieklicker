"""Easteregg "Die Zahl der Erleuchtung".

Auf dem Cookie stehen Ziffern. Wer sie in der Reihenfolge von
einstellungen.ERLEUCHTUNGS_CODE drückt, darf die geheime Glückwunschseite sehen.
Den Code verrät die Infotafel erst, wenn man den höchsten Rang erreicht hat.
Man kann ihn aber auch vorher schon eingeben, wenn man ihn kennt.
"""

from typing import Optional

import einstellungen
from app.logik.rang_system import RangSystem


class Erleuchtung:
    def __init__(self, raenge: RangSystem, code: str = None):
        self.raenge = raenge
        self.code = code or einstellungen.ERLEUCHTUNGS_CODE

    def code_passt(self, gedrueckte_ziffern: str) -> bool:
        """True, wenn die zuletzt gedrückten Ziffern genau den Code ergeben.

        Der Browser schickt die Ziffern, die seit dem letzten Klick ohne Ziffer
        gedrückt wurden. Es zählt das Ende der Eingabe: "4467911" passt also auch.
        """
        if not gedrueckte_ziffern.isdigit():
            return False
        return gedrueckte_ziffern.endswith(self.code)

    def ist_erleuchtet(self, geloeste_aufgaben: int) -> bool:
        """Höchster Rang erreicht? (Es gibt keinen nächsten Rang mehr.)"""
        return self.raenge.naechster(geloeste_aufgaben) is None

    def hinweis(self, geloeste_aufgaben: int) -> Optional[str]:
        """Text für die Infotafel, aber nur für erleuchtete Spieler, sonst None."""
        if not self.ist_erleuchtet(geloeste_aufgaben):
            return None
        return einstellungen.ERLEUCHTUNGS_HINWEIS.format(code=self.code)
