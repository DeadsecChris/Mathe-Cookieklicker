"""Tests der Spiellogik (ohne Datenbank).  Start:  python -m unittest"""

import random
import unittest
from decimal import Decimal

import einstellungen
from app.logik.aufgaben_generator import AufgabenGenerator
from app.logik.erleuchtung import Erleuchtung
from app.logik.klick_pruefer import KlickPruefer
from app.logik.rang_system import RangSystem
from app.logik.rechenaufgabe import Rechenaufgabe
from app.logik.schwierigkeitsgrad import Stufenliste
from app.logik.shop import Shop


class AufgabenTest(unittest.TestCase):
    def test_regeln_je_stufe(self):
        generator = AufgabenGenerator(zufall=random.Random(1))
        for stufe in Stufenliste()._stufen:
            komma_gesehen = False
            for _ in range(300):
                aufgabe = generator.aufgabe_fuer_stufe(stufe)
                self.assertEqual(len(aufgabe.zahlen), stufe.anzahl_zahlen)
                self.assertTrue(set(aufgabe.operationen) <= set(stufe.operationen))
                self.assertTrue(all(stufe.zahlen_von <= z <= stufe.zahlen_bis for z in aufgabe.zahlen))
                if not stufe.negativ_erlaubt:
                    self.assertFalse(aufgabe.loesung.startswith("-"), aufgabe.text)
                hat_komma = any(z != z.to_integral() for z in aufgabe.zahlen)
                if hat_komma:
                    komma_gesehen = True
                    # Kommazahlen nur ab KOMMA_AB_STUFE, nur bei Plus/Minus, eine Stelle
                    self.assertTrue(stufe.komma_erlaubt, aufgabe.text)
                    self.assertTrue(set(aufgabe.operationen) <= {"+", "-"}, aufgabe.text)
                    self.assertTrue(all(-z.as_tuple().exponent <= einstellungen.NACHKOMMASTELLEN for z in aufgabe.zahlen))
                if "/" in aufgabe.operationen:
                    # Geteilt geht immer glatt auf
                    self.assertNotIn(".", aufgabe.loesung, aufgabe.text)
            if stufe.komma_erlaubt and set(stufe.operationen) & {"+", "-"}:
                self.assertTrue(komma_gesehen, f"Stufe {stufe.nummer} ohne Kommaaufgabe")

    def test_punkt_vor_strich(self):
        self.assertEqual(AufgabenGenerator.berechnen([2, 3, 4], ["+", "*"]), 14)
        self.assertEqual(AufgabenGenerator.berechnen([10, 4, 2], ["-", "/"]), 8)

    def test_geteilt_nur_glatt(self):
        self.assertIsNone(AufgabenGenerator.berechnen([7, 2], ["/"]))
        self.assertEqual(AufgabenGenerator.berechnen([8, 2], ["/"]), 4)

    def test_antwort_pruefen(self):
        aufgabe = Rechenaufgabe([Decimal("12.5"), Decimal("3.7")], ["+"], "16.2", stufe=4)
        self.assertEqual(aufgabe.text, "12,5 + 3,7 = ?")
        self.assertTrue(aufgabe.ist_richtig("16,2"))
        self.assertTrue(aufgabe.ist_richtig(" 16.20 "))
        self.assertFalse(aufgabe.ist_richtig("16"))
        self.assertFalse(aufgabe.ist_richtig("abc"))
        ganz = Rechenaufgabe([Decimal(5), Decimal(8)], ["-"], "-3", stufe=4)
        self.assertTrue(ganz.ist_richtig("−3"))
        self.assertFalse(ganz.ist_richtig("-3.4"))

    def test_speichern_und_laden(self):
        aufgabe = Rechenaufgabe([Decimal("12.5"), Decimal("3")], ["-"], "9.5", stufe=4)
        wieder = Rechenaufgabe.aus_dict(aufgabe.als_dict())
        self.assertEqual(wieder.text, aufgabe.text)
        self.assertTrue(wieder.ist_richtig("9,5"))

    def test_stufe_steigt(self):
        liste = Stufenliste()
        self.assertEqual(liste.stufe_fuer(0).nummer, 1)
        self.assertEqual(liste.stufe_fuer(5).nummer, 2)
        self.assertEqual(liste.stufe_fuer(999).nummer, len(einstellungen.STUFEN))


class RangTest(unittest.TestCase):
    def test_rang_kommt_aus_der_stufe(self):
        liste = Stufenliste([
            {"ab_geloest": 0, "zahlen_von": 1, "zahlen_bis": 9, "operationen": ["+"], "anzahl_zahlen": 2, "rang": "A"},
            {"ab_geloest": 5, "zahlen_von": 1, "zahlen_bis": 9, "operationen": ["+"], "anzahl_zahlen": 2, "rang": "B"},
        ])
        raenge = RangSystem(liste)
        self.assertEqual(raenge.rang(0), "A")
        self.assertEqual(raenge.naechster(0), ("B", 5))
        self.assertEqual(raenge.rang(7), "B")
        self.assertIsNone(raenge.naechster(7))

    def test_jede_stufe_hat_einen_rang(self):
        for eintrag in einstellungen.STUFEN:
            self.assertTrue(eintrag.get("rang"), eintrag)


class ShopTest(unittest.TestCase):
    def test_preis_steigt(self):
        shop = Shop(startpreis=10, preisfaktor=1.5)
        self.assertEqual([shop.preis(n) for n in range(4)], [10, 15, 22, 34])


class ZuwachsTest(unittest.TestCase):
    def test_zuwachs_multipliziert(self):
        from app.logik.spiel import Spiel
        alt = einstellungen.ZUWACHS_FAKTOR
        try:
            einstellungen.ZUWACHS_FAKTOR = 1.5
            werte = [1]
            for _ in range(5):
                werte.append(werte[-1] + Spiel.zuwachs(werte[-1]))
            self.assertEqual(werte, [1, 2, 3, 4, 6, 9])
            einstellungen.ZUWACHS_FAKTOR = 1
            self.assertEqual(Spiel.zuwachs(7), 1)   # mindestens +1
        finally:
            einstellungen.ZUWACHS_FAKTOR = alt


class SpielstandTest(unittest.TestCase):
    """naechster_zuwachs im Spielstand (ohne Datenbank, mit einem Speicher-Ersatz)."""

    class Ersatzspeicher:
        def speichern(self, spieler):
            pass

    def test_naechster_zuwachs(self):
        from app.logik.spiel import Spiel
        from app.logik.spieler import Spieler
        alt = einstellungen.ZUWACHS_FAKTOR
        try:
            einstellungen.ZUWACHS_FAKTOR = 1.4
            spiel = Spiel(self.Ersatzspeicher())
            spieler = Spieler(benutzername="test", passwort_hash="x", cookies_pro_klick=8)
            self.assertEqual(spiel.spielstand(spieler)["naechster_zuwachs"], 3)
            spieler.cookies_pro_klick = 11
            self.assertEqual(spiel.spielstand(spieler)["naechster_zuwachs"], 4)

            # Nach einer richtigen Antwort passt der Wert zu den neuen Cookies pro Klick
            spieler.offene_aufgabe = Rechenaufgabe([Decimal(2), Decimal(3)], ["+"], "5", stufe=1)
            stand = spiel.aufgabe_beantworten(spieler, "5")
            self.assertTrue(stand["richtig"])
            self.assertEqual(stand["cookies_pro_klick"], 15)
            self.assertEqual(stand["naechster_zuwachs"], Spiel.zuwachs(15))
        finally:
            einstellungen.ZUWACHS_FAKTOR = alt

    def test_negative_zahl_in_klammern(self):
        aufgabe = Rechenaufgabe([Decimal(5), Decimal(-3)], ["-"], "8", stufe=6)
        self.assertEqual(aufgabe.text, "5 − (−3) = ?")


class KlickPrueferTest(unittest.TestCase):
    def test_menschliche_klicks(self):
        zufall = random.Random(3)
        zeit, zeiten = 0.0, []
        for _ in range(40):
            zeit += zufall.uniform(90, 250)
            zeiten.append(zeit)
        self.assertTrue(KlickPruefer().pruefen(zeiten).gueltig)

    def test_zu_schnell(self):
        zeiten = [i * 20.0 + (i % 3) for i in range(30)]   # 50 pro Sekunde
        self.assertFalse(KlickPruefer().pruefen(zeiten).gueltig)

    def test_gleichmaessig(self):
        zeiten = [i * 100.0 for i in range(30)]           # exakt alle 100 ms
        ergebnis = KlickPruefer().pruefen(zeiten)
        self.assertFalse(ergebnis.gueltig)
        self.assertIn("gleichmäßig", ergebnis.grund)


class ErleuchtungTest(unittest.TestCase):
    """Easteregg: Zahl der Erleuchtung."""

    def setUp(self):
        self.erleuchtung = Erleuchtung(RangSystem(), code="67911")

    def test_code_passt(self):
        self.assertTrue(self.erleuchtung.code_passt("67911"))
        self.assertTrue(self.erleuchtung.code_passt("4467911"))   # davor vertippt
        self.assertFalse(self.erleuchtung.code_passt("6791"))
        self.assertFalse(self.erleuchtung.code_passt("679110"))
        self.assertFalse(self.erleuchtung.code_passt(""))
        self.assertFalse(self.erleuchtung.code_passt("6791x1"))

    def test_hinweis_nur_beim_hoechsten_rang(self):
        letzte_schwelle = einstellungen.STUFEN[-1]["ab_geloest"]
        self.assertIsNone(self.erleuchtung.hinweis(0))
        self.assertIsNone(self.erleuchtung.hinweis(letzte_schwelle - 1))
        hinweis = self.erleuchtung.hinweis(letzte_schwelle)
        self.assertIn("67911", hinweis)
        self.assertIn("erleuchtete Cookieherrscher", hinweis)

    def test_spieler_wird_erleuchtet_und_gespeichert(self):
        from app.logik.spiel import Spiel
        from app.logik.spieler import Spieler

        class Speicher:
            def __init__(self): self.gespeichert = 0
            def speichern(self, spieler): self.gespeichert += 1

        speicher = Speicher()
        spiel = Spiel(speicher)
        spieler = Spieler("test", "hash")
        self.assertFalse(spiel.erleuchtung_pruefen(spieler, "6791")["erleuchtet"])
        stand = spiel.erleuchtung_pruefen(spieler, einstellungen.ERLEUCHTUNGS_CODE)
        self.assertTrue(stand["gefunden"])
        self.assertTrue(stand["erleuchtet"])
        self.assertEqual(speicher.gespeichert, 1)
        # bleibt nach dem Laden aus der Datenbank erhalten, Zurücksetzen nimmt es weg
        self.assertTrue(Spieler.aus_dict(spieler.als_dict()).erleuchtet)
        spieler.zuruecksetzen()
        self.assertFalse(spieler.erleuchtet)

    def test_standardcode_nur_aus_ziffern_auf_dem_cookie(self):
        self.assertTrue(set(einstellungen.ERLEUCHTUNGS_CODE) <= set("679140"))


if __name__ == "__main__":
    unittest.main()
