"""FastAPI-Anwendung: baut alle Teile zusammen.

Start über start.py (oder direkt: python -m uvicorn app.main:erstelle_app --factory).
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.datenbank.spieler_repository import SpielerRepository
from app.logik.spiel import Spiel
from app.routen import konto, seiten, spiel
from app.sitzungen import Sitzungsverwaltung

STATIC = Path(__file__).resolve().parent.parent / "static"


def erstelle_app(repository: SpielerRepository = None) -> FastAPI:
    app = FastAPI(title="Mathecookie")
    app.state.repository = repository or SpielerRepository.mit_lokaler_datenbank()
    app.state.spiel = Spiel(app.state.repository)
    app.state.sitzungen = Sitzungsverwaltung()

    app.include_router(seiten.router)
    app.include_router(konto.router)
    app.include_router(spiel.router)
    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app

