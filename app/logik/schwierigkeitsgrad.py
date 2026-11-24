"""Ein Schwierigkeitsgrad (eine Stufe) und die Auswahl der passenden Stufe."""

from dataclasses import dataclass

import einstellungen


@dataclass(frozen=True)
class Schwierigkeitsgrad:
    """Legt fest, wie eine Rechenaufgabe einer Stufe aussehen darf."""

    nummer: int
    ab_geloest: int
    zahlen_von: int
    zahlen_bis: int
    operationen: tuple
    anzahl_zahlen: int
    rang: str = ""

    @property
    def negativ_erlaubt(self) -> bool:
        return self.nummer >= einstellungen.NEGATIV_AB_STUFE

    @property
    def komma_erlaubt(self) -> bool:
        return self.nummer >= einstellungen.KOMMA_AB_STUFE


class Stufenliste:
    """Alle Stufen aus den Einstellungen. Wählt die Stufe passend zu den gelösten Aufgaben."""

    def __init__(self, stufen_daten=None):
        daten = stufen_daten if stufen_daten is not None else einstellungen.STUFEN
        self._stufen = [
            Schwierigkeitsgrad(
                nummer=index + 1,
                ab_geloest=eintrag["ab_geloest"],
                zahlen_von=eintrag["zahlen_von"],
                zahlen_bis=eintrag["zahlen_bis"],
                operationen=tuple(eintrag["operationen"]),
                anzahl_zahlen=eintrag["anzahl_zahlen"],
                rang=eintrag.get("rang", f"Stufe {index + 1}"),
            )
            for index, eintrag in enumerate(daten)
        ]

    def stufe_fuer(self, geloeste_aufgaben: int) -> Schwierigkeitsgrad:
        """Höchste Stufe, deren Schwelle schon erreicht ist."""
        passende = self._stufen[0]
        for stufe in self._stufen:
            if geloeste_aufgaben >= stufe.ab_geloest:
                passende = stufe
        return passende

    def naechste_stufe(self, stufe: Schwierigkeitsgrad):
        """Die Stufe nach der angegebenen oder None, wenn es die höchste ist."""
        if stufe.nummer < len(self._stufen):
            return self._stufen[stufe.nummer]
        return None
