"""Eine einzelne Rechenaufgabe: Text, Lösung und Prüfung der Antwort."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

ANZEIGE_ZEICHEN = {"+": "+", "-": "−", "*": "×", "/": "÷"}


@dataclass
class Rechenaufgabe:
    """Zahlen und Lösung werden als Decimal bzw. Text gespeichert, damit Kommazahlen exakt bleiben."""

    zahlen: list
    operationen: list
    loesung: str
    stufe: int

    @property
    def text(self) -> str:
        teile = [self._anzeigen(self.zahlen[0])]
        for operation, zahl in zip(self.operationen, self.zahlen[1:]):
            teile.append(ANZEIGE_ZEICHEN[operation])
            teile.append(self._anzeigen(zahl))
        return " ".join(teile) + " = ?"

    @staticmethod
    def _anzeigen(zahl) -> str:
        """Deutsche Schreibweise mit Komma, ganze Zahlen ohne ",0"."""
        zahl = Decimal(zahl)
        if zahl == zahl.to_integral():
            text = str(int(zahl))
        else:
            text = str(zahl).replace(".", ",")
        if zahl < 0:                       # negative Zahlen in Klammern: 5 − (−3)
            text = "(−" + text[1:] + ")"
        return text

    def ist_richtig(self, antwort: str) -> bool:
        """Vergleicht die Eingabe exakt mit der Lösung. Komma und Punkt sind beide erlaubt."""
        zahl = self.eingabe_lesen(antwort)
        return zahl is not None and zahl == Decimal(self.loesung)

    @staticmethod
    def eingabe_lesen(antwort: str):
        bereinigt = str(antwort).strip().replace(" ", "").replace(",", ".").replace("−", "-")
        if not bereinigt:
            return None
        try:
            zahl = Decimal(bereinigt)
        except InvalidOperation:
            return None
        return zahl if zahl.is_finite() else None

    # Speichern in der Datenbank (Zahlen als Text, MongoDB kennt kein Decimal)

    def als_dict(self) -> dict:
        return {
            "zahlen": [str(zahl) for zahl in self.zahlen],
            "operationen": self.operationen,
            "loesung": self.loesung,
            "stufe": self.stufe,
        }

    @classmethod
    def aus_dict(cls, daten: dict) -> "Rechenaufgabe":
        return cls(
            zahlen=[Decimal(str(zahl)) for zahl in daten["zahlen"]],
            operationen=list(daten["operationen"]),
            loesung=daten["loesung"],
            stufe=daten["stufe"],
        )
