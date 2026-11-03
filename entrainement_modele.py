
import sqlite3
import pickle
from encodage_date import encoder_date
from datetime import datetime

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    brier_score_loss
)

# Lire les données nettoyées
connexion = sqlite3.connect("meteo_paris.db")

donnees = connexion.execute("""
    SELECT date_jour, pluie
    FROM pluie_quotidienne_v2
    WHERE station = '000CT'
    ORDER BY date_jour
""").fetchall()

connexion.close()

# Préparer les données
X_train, X_test = [], []
y_train, y_test = [], []
mois_train, mois_test = [], []

for date_jour, pluie in donnees:
    date_objet = datetime.strptime(date_jour, "%Y-%m-%d").date()
    variables = encoder_date(date_objet)

    if date_objet < datetime(2025, 11, 1).date():
        X_train.append(variables)
        y_train.append(pluie)
        mois_train.append(date_objet.month)
    else:
        X_test.append(variables)
        y_test.append(pluie)
        mois_test.append(date_objet.month)

print("Journées d'entraînement :", len(X_train))
print("Journées de test :", len(X_test))

# Entraîner le modèle
modele = LogisticRegression(max_iter=1000)
modele.fit(X_train, y_train)

# Prédictions sur les dates de test
probabilites = modele.predict_proba(X_test)[:, 1]
predictions = modele.predict(X_test)

# Référence : fréquence mensuelle de pluie
frequence_globale = np.mean(y_train)
frequences_mensuelles = {}

for mois in range(1, 13):
    valeurs = [
        pluie for m, pluie in zip(mois_train, y_train)
        if m == mois
    ]
    frequences_mensuelles[mois] = (
        np.mean(valeurs) if valeurs else frequence_globale
    )

probabilites_reference = np.array([
    frequences_mensuelles[mois] for mois in mois_test
])
predictions_reference = (
    probabilites_reference >= 0.5
).astype(int)

# Évaluer les deux méthodes
def evaluer(nom, y_reel, pred, proba):
    print("\nRésultats :", nom)
    print("Accuracy :", round(accuracy_score(y_reel, pred), 3))
    print("Précision :", round(
        precision_score(y_reel, pred, zero_division=0), 3
    ))
    print("Rappel :", round(
        recall_score(y_reel, pred, zero_division=0), 3
    ))
    print("F1-score :", round(
        f1_score(y_reel, pred, zero_division=0), 3
    ))
    print("ROC-AUC :", round(
        roc_auc_score(y_reel, proba), 3
    ))
    print("Brier score :", round(
        brier_score_loss(y_reel, proba), 3
    ))

evaluer("Régression logistique", y_test, predictions, probabilites)
evaluer(
    "Référence mensuelle",
    y_test,
    predictions_reference,
    probabilites_reference
)

# Sauvegarder le modèle et ses paramètres
with open("modele_pluie.pkl", "wb") as fichier:
    pickle.dump({
        "modele": modele,
        "frequences_mensuelles": frequences_mensuelles,
        "station": "000CT",
        "seuil_pluie_mm": 1.0
    }, fichier)

print("\nModèle sauvegardé dans modele_pluie.pkl")

# Examiner les probabilités estimées
print("Probabilité minimale :", round(min(probabilites), 3))
print("Probabilité maximale :", round(max(probabilites), 3))
print("Probabilité moyenne :", round(float(np.mean(probabilites)), 3))


# Tester le risque de pluie selon les saisons
dates_test = [
    "2027-01-15",
    "2027-04-15",
    "2027-07-15",
    "2027-10-15"
]

print("\nEstimations pour quatre dates futures :")

for date_texte in dates_test:
    date_objet = datetime.strptime(date_texte, "%Y-%m-%d").date()
    variables = encoder_date(date_objet)

    risque = modele.predict_proba([variables])[0][1] * 100

    print(date_texte, ":", round(risque, 1), "%")


# Test complémentaire avec un seuil de 30 %
print("\nRésultats avec un seuil de 30 % :")

predictions_30 = (probabilites >= 0.30).astype(int)

evaluer(
    "Régression logistique - seuil 30 %",
    y_test,
    predictions_30,
    probabilites
)

print("Journées prédites pluvieuses :", sum(predictions_30))
print("Journées réellement pluvieuses :", sum(y_test))


# Comparaison de la référence mensuelle au seuil de 30 %
print("\nRésultats de la référence mensuelle avec un seuil de 30 % :")

predictions_reference_30 = (
    probabilites_reference >= 0.30
).astype(int)

evaluer(
    "Référence mensuelle - seuil 30 %",
    y_test,
    predictions_reference_30,
    probabilites_reference
)

print(
    "Journées prédites pluvieuses :",
    sum(predictions_reference_30)
)
