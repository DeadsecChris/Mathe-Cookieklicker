"""Liest und schreibt Spieler in der MongoDB-Sammlung "spieler"."""

from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection

import einstellungen
from app.logik.spieler import Spieler


class SpielerRepository:
    def __init__(self, sammlung: Collection):
        self.sammlung = sammlung
        self.sammlung.create_index("benutzername", unique=True)

    @classmethod
    def mit_lokaler_datenbank(cls) -> "SpielerRepository":
        client = MongoClient(einstellungen.MONGO_HOST, einstellungen.MONGO_PORT, serverSelectionTimeoutMS=3000)
        return cls(client[einstellungen.DATENBANK_NAME]["spieler"])

    def laden(self, benutzername: str) -> Optional[Spieler]:
        daten = self.sammlung.find_one({"benutzername": benutzername})
        return Spieler.aus_dict(daten) if daten else None

    def neu_anlegen(self, spieler: Spieler):
        self.sammlung.insert_one(spieler.als_dict())

    def speichern(self, spieler: Spieler):
        self.sammlung.replace_one({"benutzername": spieler.benutzername}, spieler.als_dict())
