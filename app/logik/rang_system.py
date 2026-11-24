"""Ränge: Jede Stufe hat einen Rangnamen (Feld "rang" in einstellungen.STUFEN).

Man steigt mit richtig gelösten Aufgaben auf. Gelöste Aufgaben werden nie
weniger, deshalb sinkt der Rang nie (außer beim Zurücksetzen).
"""

from app.logik.schwierigkeitsgrad import Stufenliste


class RangSystem:
    def __init__(self, stufenliste: Stufenliste = None):
        self.stufenliste = stufenliste or Stufenliste()

    def rang(self, geloeste_aufgaben: int) -> str:
        return self.stufenliste.stufe_fuer(geloeste_aufgaben).rang

    def naechster(self, geloeste_aufgaben: int):
        """(Rangname, ab wie vielen gelösten Aufgaben) des nächsten Rangs oder None."""
        stufe = self.stufenliste.stufe_fuer(geloeste_aufgaben)
        naechste = self.stufenliste.naechste_stufe(stufe)
        if naechste is None:
            return None
        return naechste.rang, naechste.ab_geloest
