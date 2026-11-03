
import os
import time
import sqlite3
from datetime import date, timedelta

import requests
from dotenv import load_dotenv

# Charger la clé API
load_dotenv()
cle_api = os.getenv("INFOCLIMAT_API_KEY")

if not cle_api:
    raise SystemExit("Clé API Infoclimat introuvable.")

# Configuration Infoclimat
station = "000CT"
url_api = "https://www.infoclimat.fr/opendata/"

# Historique de trois ans
date_debut = date(2023, 11, 1)
date_fin = date(2026, 10, 31)

# Ouvrir la base existante
connexion = sqlite3.connect("meteo_paris.db")

# Table des précipitations horaires
connexion.execute("""
CREATE TABLE IF NOT EXISTS precipitations (
    station TEXT,
    date_heure TEXT,
    pluie_1h REAL,
    PRIMARY KEY (station, date_heure)
)
""")

# Table des précipitations quotidiennes
connexion.execute("""
CREATE TABLE IF NOT EXISTS pluie_quotidienne_v2 (
    station TEXT,
    date_jour TEXT,
    pluie_mm REAL,
    pluie INTEGER,
    PRIMARY KEY (station, date_jour)
)
""")

debut = date_debut

try:
    # Collecte par périodes de 7 jours
    while debut <= date_fin:
        fin = min(debut + timedelta(days=6), date_fin)

        print("Collecte du", debut, "au", fin)

        parametres = {
            "version": 2,
            "method": "get",
            "format": "json",
            "stations[]": station,
            "start": debut.isoformat(),
            "end": fin.isoformat(),
            "token": cle_api
        }

        try:
            reponse = requests.get(
                url_api, params=parametres, timeout=30
            )
            reponse.raise_for_status()
            donnees = reponse.json()
        except (requests.RequestException, ValueError) as erreur:
            print("Erreur de collecte :", erreur)
            break

        if donnees.get("status") != "OK":
            print("Erreur API :", donnees.get("errors"))
            break

        releves = donnees.get("hourly", {}).get(station, [])
        compteur = 0

        for r in releves:
            pluie = r.get("pluie_1h")
            heure = r.get("dh_utc", "")

            if (
                heure.endswith("00:00")
                and isinstance(pluie, (int, float))
            ):
                connexion.execute("""
                    INSERT OR IGNORE INTO precipitations
                    (station, date_heure, pluie_1h)
                    VALUES (?, ?, ?)
                """, (station, heure, pluie))
                compteur += 1

        connexion.commit()
        print("Mesures de pluie disponibles :", compteur)

        debut = fin + timedelta(days=1)

        if debut <= date_fin:
            time.sleep(1)

    # Créer les observations quotidiennes exploitables
    connexion.execute("""
        INSERT OR REPLACE INTO pluie_quotidienne_v2
        (station, date_jour, pluie_mm, pluie)
        SELECT
            station,
            substr(date_heure, 1, 10),
            SUM(pluie_1h),
            CASE WHEN SUM(pluie_1h) >= 1 THEN 1 ELSE 0 END
        FROM precipitations
        WHERE station = ?
        GROUP BY station, substr(date_heure, 1, 10)
        HAVING COUNT(DISTINCT substr(date_heure, 12, 2)) >= 20
    """, (station,))

    connexion.commit()

    total = connexion.execute(
        "SELECT COUNT(*) FROM precipitations WHERE station = ?",
        (station,)
    ).fetchone()[0]

    jours = connexion.execute(
        "SELECT COUNT(*) FROM pluie_quotidienne_v2 WHERE station = ?",
        (station,)
    ).fetchone()[0]

    print("Mesures horaires en base :", total)
    print("Journées exploitables :", jours)

    # Compter les journées pluvieuses et sèches
    pluvieux = connexion.execute(
        "SELECT COUNT(*) FROM pluie_quotidienne_v2 WHERE station = ? AND pluie = 1",
        (station,)
    ).fetchone()[0]

    secs = jours - pluvieux

    print("Journées pluvieuses :", pluvieux)
    print("Journées sèches :", secs)

    print("Programme terminé !")

finally:
    connexion.close()
