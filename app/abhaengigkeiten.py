"""Gemeinsame Objekte für alle Routen (werden in main.py einmal erzeugt)."""

from fastapi import HTTPException, Request

from app.logik.spieler import Spieler
from app.sitzungen import COOKIE_NAME


def aktueller_benutzername(request: Request):
    return request.app.state.sitzungen.benutzer(request.cookies.get(COOKIE_NAME))


def aktueller_spieler(request: Request) -> Spieler:
    """Für API-Routen: angemeldeten Spieler laden, sonst Fehler 401."""
    benutzername = aktueller_benutzername(request)
    spieler = request.app.state.repository.laden(benutzername) if benutzername else None
    if spieler is None:
        raise HTTPException(status_code=401, detail="Nicht angemeldet.")
    return spieler
