"""Erzeugt zufällige Rechenaufgaben passend zur Stufe."""

import random
from decimal import Decimal
from fractions import Fraction

import einstellungen
from app.logik.rechenaufgabe import Rechenaufgabe
from app.logik.schwierigkeitsgrad import Schwierigkeitsgrad, Stufenliste

MAX_VERSUCHE = 2000
PLUS_MINUS = {"+", "-"}


class AufgabenGenerator:
    """Würfelt Aufgaben, bis eine die Regeln der Stufe erfüllt."""

    def __init__(self, stufenliste: Stufenliste = None, zufall: random.Random = None):
        self.stufenliste = stufenliste or Stufenliste()
        self.zufall = zufall or random.Random()

    def neue_aufgabe(self, geloeste_aufgaben: int) -> Rechenaufgabe:
        stufe = self.stufenliste.stufe_fuer(geloeste_aufgaben)
        return self.aufgabe_fuer_stufe(stufe)

    def aufgabe_fuer_stufe(self, stufe: Schwierigkeitsgrad) -> Rechenaufgabe:
        for _ in range(MAX_VERSUCHE):
            operationen = [self.zufall.choice(stufe.operationen) for _ in range(stufe.anzahl_zahlen - 1)]
            mit_komma = self._mit_komma(stufe, operationen)
            zahlen = [self._zufallszahl(stufe, mit_komma) for _ in range(stufe.anzahl_zahlen)]
            ergebnis = self.berechnen(zahlen, operationen)
            if ergebnis is not None and self._erlaubt(ergebnis, stufe):
                return Rechenaufgabe(zahlen=zahlen, operationen=operationen, loesung=self._als_text(ergebnis), stufe=stufe.nummer)
        # Sehr unwahrscheinlich, nur bei ungünstigen Einstellungen: einfache Plus-Aufgabe.
        zahlen = [Decimal(stufe.zahlen_von), Decimal(stufe.zahlen_bis)]
        return Rechenaufgabe(zahlen=zahlen, operationen=["+"], loesung=str(sum(zahlen)), stufe=stufe.nummer)

    def _mit_komma(self, stufe: Schwierigkeitsgrad, operationen: list) -> bool:
        """Kommazahlen nur ab KOMMA_AB_STUFE und nur bei reinen Plus/Minus-Aufgaben."""
        if not stufe.komma_erlaubt or not set(operationen) <= PLUS_MINUS:
            return False
        return self.zufall.random() < einstellungen.KOMMA_ANTEIL

    def _zufallszahl(self, stufe: Schwierigkeitsgrad, mit_komma: bool) -> Decimal:
        if not mit_komma:
            return Decimal(self.zufall.randint(stufe.zahlen_von, stufe.zahlen_bis))
        faktor = 10 ** einstellungen.NACHKOMMASTELLEN
        ganz = self.zufall.randint(stufe.zahlen_von * faktor, stufe.zahlen_bis * faktor)
        return Decimal(ganz).scaleb(-einstellungen.NACHKOMMASTELLEN)

    @staticmethod
    def berechnen(zahlen, operationen):
        """Rechnet exakt, Punkt vor Strich.

        Gibt None zurück, wenn eine Geteilt-Rechnung nicht glatt aufgeht
        (oder durch 0 geteilt würde). Solche Aufgaben werden neu gewürfelt.
        """
        werte = [Fraction(zahlen[0])]
        zeichen = []
        for operation, zahl in zip(operationen, zahlen[1:]):
            if operation == "*":
                werte[-1] *= Fraction(zahl)
            elif operation == "/":
                if zahl == 0:
                    return None
                werte[-1] /= Fraction(zahl)
                if werte[-1].denominator != 1:
                    return None
            else:
                werte.append(Fraction(zahl))
                zeichen.append(operation)
        ergebnis = werte[0]
        for operation, wert in zip(zeichen, werte[1:]):
            ergebnis = ergebnis + wert if operation == "+" else ergebnis - wert
        return ergebnis

    @staticmethod
    def _erlaubt(ergebnis: Fraction, stufe: Schwierigkeitsgrad) -> bool:
        return ergebnis >= 0 or stufe.negativ_erlaubt

    @staticmethod
    def _als_text(ergebnis: Fraction) -> str:
        """Bruch -> Dezimaltext, z. B. 73/10 -> "7.3". Geht immer auf, da nur Zehntel & Co. vorkommen."""
        wert = Decimal(ergebnis.numerator) / Decimal(ergebnis.denominator)
        return str(wert.normalize()) if wert != wert.to_integral() else str(wert.to_integral())
