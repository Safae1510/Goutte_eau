
from datetime import date
from pathlib import Path
import pickle

from fastapi import FastAPI
from encodage_date import encoder_date

# Charger notre modèle d'IA sauvegardé
chemin_modele = Path(__file__).parent / "modele_pluie.pkl"

with open(chemin_modele, "rb") as fichier:
    donnees_modele = pickle.load(fichier)

modele = donnees_modele["modele"]

# Créer notre API
app = FastAPI(
    title="Goutte d'Eau - API",
    description="Estimation du risque statistique de pluie à Paris",
    version="1.0"
)


@app.get("/")
def accueil():
    return {
        "projet": "Goutte d'Eau",
        "message": "API opérationnelle"
    }


@app.get("/prediction")
def prediction(date_prevision: date):
    # Encoder la date exactement comme pendant l'entraînement
    variables = encoder_date(date_prevision)

    # Calculer la probabilité de pluie
    probabilite = modele.predict_proba([variables])[0][1]

    return {
        "date": date_prevision.isoformat(),
        "station": donnees_modele["station"],
        "risque_pluie_pourcentage": round(float(probabilite) * 100, 1),
        "seuil_pluie_mm": donnees_modele["seuil_pluie_mm"]
    }
