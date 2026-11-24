"""Die HTML-Seiten. Ohne Anmeldung geht es immer zurück zur Anmeldeseite."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse

from app.abhaengigkeiten import aktueller_benutzername

SEITEN = Path(__file__).resolve().parent.parent.parent / "static"

router = APIRouter()

# Seiten nie aus dem Browser-Cache holen, sonst sieht man sie nach dem Abmelden noch.
KEIN_CACHE = {"Cache-Control": "no-store"}


@router.get("/")
def anmeldeseite(request: Request):
    if aktueller_benutzername(request):
        return RedirectResponse("/hauptmenue")
    return FileResponse(SEITEN / "anmeldung.html", headers=KEIN_CACHE)


@router.get("/hauptmenue")
def hauptmenue(request: Request):
    if not aktueller_benutzername(request):
        return RedirectResponse("/")
    return FileResponse(SEITEN / "hauptmenue.html", headers=KEIN_CACHE)


@router.get("/spiel")
def cookie_klickseite(request: Request):
    if not aktueller_benutzername(request):
        return RedirectResponse("/")
    return FileResponse(SEITEN / "spiel.html", headers=KEIN_CACHE)

