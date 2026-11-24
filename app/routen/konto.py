"""Registrieren, Anmelden, Abmelden."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.logik.benutzerverwaltung import AnmeldeFehler, Benutzerverwaltung
from app.sitzungen import COOKIE_NAME

router = APIRouter(prefix="/api/konto")


class Registrierung(BaseModel):
    benutzername: str
    passwort: str
    passwort_bestaetigen: str


class Anmeldung(BaseModel):
    benutzername: str
    passwort: str


def _angemeldet_antwort(request: Request, benutzername: str) -> JSONResponse:
    schluessel = request.app.state.sitzungen.starten(benutzername)
    # Nach der Anmeldung geht es immer zuerst ins Hauptmenü (Vorgabe vom Lehrer).
    antwort = JSONResponse({"weiter": "/hauptmenue"})
    antwort.set_cookie(COOKIE_NAME, schluessel, httponly=True, samesite="strict")
    return antwort


@router.get("/passwortregel")
def passwortregel():
    return {"regel": Benutzerverwaltung.passwort_regel_text()}


@router.post("/registrieren")
def registrieren(daten: Registrierung, request: Request):
    verwaltung = Benutzerverwaltung(request.app.state.repository)
    try:
        spieler = verwaltung.registrieren(daten.benutzername, daten.passwort, daten.passwort_bestaetigen)
    except AnmeldeFehler as fehler:
        raise HTTPException(status_code=400, detail=str(fehler))
    return _angemeldet_antwort(request, spieler.benutzername)


@router.post("/anmelden")
def anmelden(daten: Anmeldung, request: Request):
    verwaltung = Benutzerverwaltung(request.app.state.repository)
    try:
        spieler = verwaltung.anmelden(daten.benutzername, daten.passwort)
    except AnmeldeFehler as fehler:
        raise HTTPException(status_code=400, detail=str(fehler))
    return _angemeldet_antwort(request, spieler.benutzername)


@router.post("/abmelden")
def abmelden(request: Request):
    request.app.state.sitzungen.beenden(request.cookies.get(COOKIE_NAME))
    antwort = JSONResponse({"weiter": "/"})
    antwort.delete_cookie(COOKIE_NAME)
    return antwort
