"""Spielaktionen. Die Routen sind bewusst dünn, die Logik steckt in der Klasse Spiel."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.abhaengigkeiten import aktueller_spieler
from app.logik.spiel import SpielFehler
from app.logik.spieler import Spieler

router = APIRouter(prefix="/api/spiel")


class Klickpaket(BaseModel):
    zeitstempel: List[float]


class Antwort(BaseModel):
    antwort: str


class Ziffern(BaseModel):
    ziffern: str


def _spiel(request: Request):
    return request.app.state.spiel


@router.get("/stand")
def spielstand(request: Request, spieler: Spieler = Depends(aktueller_spieler)):
    return _spiel(request).spielstand(spieler)


@router.post("/klicks")
def klicks(paket: Klickpaket, request: Request, spieler: Spieler = Depends(aktueller_spieler)):
    return _spiel(request).klicks_melden(spieler, paket.zeitstempel)


@router.post("/kaufen")
def kaufen(request: Request, spieler: Spieler = Depends(aktueller_spieler)):
    try:
        return _spiel(request).aufgabe_kaufen(spieler)
    except SpielFehler as fehler:
        raise HTTPException(status_code=400, detail=str(fehler))


@router.post("/antworten")
def antworten(daten: Antwort, request: Request, spieler: Spieler = Depends(aktueller_spieler)):
    try:
        return _spiel(request).aufgabe_beantworten(spieler, daten.antwort)
    except SpielFehler as fehler:
        raise HTTPException(status_code=400, detail=str(fehler))


@router.post("/zuruecksetzen")
def zuruecksetzen(request: Request, spieler: Spieler = Depends(aktueller_spieler)):
    return _spiel(request).zuruecksetzen(spieler)


@router.post("/erleuchtung")
def erleuchtung(daten: Ziffern, request: Request, spieler: Spieler = Depends(aktueller_spieler)):
    """Easteregg: gedrückte Ziffern auf dem Cookie prüfen."""
    return _spiel(request).erleuchtung_pruefen(spieler, daten.ziffern)
