"""Merkt sich, wer angemeldet ist (Sitzungs-Cookie im Browser -> Benutzername)."""

import secrets
from typing import Optional

COOKIE_NAME = "mathecookie_sitzung"


class Sitzungsverwaltung:
    def __init__(self):
        self._sitzungen = {}

    def starten(self, benutzername: str) -> str:
        schluessel = secrets.token_urlsafe(32)
        self._sitzungen[schluessel] = benutzername
        return schluessel

    def benutzer(self, schluessel: Optional[str]) -> Optional[str]:
        if not schluessel:
            return None
        return self._sitzungen.get(schluessel)

    def beenden(self, schluessel: Optional[str]):
        self._sitzungen.pop(schluessel, None)
