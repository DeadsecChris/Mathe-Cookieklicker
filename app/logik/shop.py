"""Kaufpreis der Rechenaufgaben. Steigt nur mit richtig gelösten Aufgaben."""

import einstellungen


class Shop:
    def __init__(self, startpreis=None, preisfaktor=None):
        self.startpreis = startpreis if startpreis is not None else einstellungen.STARTPREIS
        self.preisfaktor = preisfaktor if preisfaktor is not None else einstellungen.PREISFAKTOR

    def preis(self, geloeste_aufgaben: int) -> int:
        return max(1, round(self.startpreis * self.preisfaktor ** geloeste_aufgaben))
