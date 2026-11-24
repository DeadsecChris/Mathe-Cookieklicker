"""Prüft gesammelte Klicks auf Tempo und Rhythmus (Schutz gegen Auto-Klicker)."""

import statistics
from dataclasses import dataclass

import einstellungen


@dataclass
class Pruefergebnis:
    gueltig: bool
    grund: str = ""


class KlickPruefer:
    def __init__(self, max_pro_sekunde=None, rhythmus_min_klicks=None, rhythmus_min_streuung_ms=None):
        self.max_pro_sekunde = max_pro_sekunde or einstellungen.MAX_KLICKS_PRO_SEKUNDE
        self.rhythmus_min_klicks = rhythmus_min_klicks or einstellungen.RHYTHMUS_MIN_KLICKS
        self.rhythmus_min_streuung_ms = (
            rhythmus_min_streuung_ms
            if rhythmus_min_streuung_ms is not None
            else einstellungen.RHYTHMUS_MIN_STREUUNG_MS
        )

    def pruefen(self, zeitstempel_ms: list, sekunden_seit_letztem_paket: float = None) -> Pruefergebnis:
        """zeitstempel_ms: Zeitpunkt jedes Klicks in Millisekunden (aus dem Browser)."""
        if not zeitstempel_ms:
            return Pruefergebnis(True)
        zeiten = sorted(float(z) for z in zeitstempel_ms)

        if self._zu_schnell(zeiten):
            return Pruefergebnis(False, f"mehr als {self.max_pro_sekunde} Klicks pro Sekunde")

        # Zusätzlich mit der Server-Uhr prüfen, falls die Zeitstempel geschönt wurden.
        if sekunden_seit_letztem_paket is not None:
            erlaubt = self.max_pro_sekunde * (sekunden_seit_letztem_paket + 1)
            if len(zeiten) > erlaubt:
                return Pruefergebnis(False, f"mehr als {self.max_pro_sekunde} Klicks pro Sekunde")

        if self._zu_gleichmaessig(zeiten):
            return Pruefergebnis(False, "Klicks kommen verdächtig gleichmäßig (Auto-Klicker?)")
        return Pruefergebnis(True)

    def _zu_schnell(self, zeiten: list) -> bool:
        """Gleitendes Fenster von einer Sekunde."""
        anfang = 0
        for ende in range(len(zeiten)):
            while zeiten[ende] - zeiten[anfang] >= 1000:
                anfang += 1
            if ende - anfang + 1 > self.max_pro_sekunde:
                return True
        return False

    def _zu_gleichmaessig(self, zeiten: list) -> bool:
        if len(zeiten) < self.rhythmus_min_klicks:
            return False
        abstaende = [b - a for a, b in zip(zeiten, zeiten[1:])]
        return statistics.pstdev(abstaende) < self.rhythmus_min_streuung_ms
