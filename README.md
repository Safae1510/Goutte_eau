
# Goutte d'Eau - MVP

## Présentation du projet

Goutte d'Eau est un projet réalisé dans le cadre d'un Mastère en Transformation digitale et Intelligence artificielle.

Ce MVP propose une estimation du risque statistique de pluie à Paris à partir d'une date sélectionnée par l'utilisateur.

L'application repose sur Python, une base de données SQLite, un modèle de Machine Learning, une API FastAPI et une interface Streamlit.

## Objectif du MVP

L'objectif est de démontrer la faisabilité d'une chaîne complète de traitement des données météorologiques :

1. Collecter des données historiques.
2. Nettoyer et stocker les précipitations.
3. Entraîner et évaluer un modèle de Machine Learning.
4. Exposer le modèle à travers une API.
5. Présenter les résultats dans une interface utilisateur.

## Données utilisées

- Source : Infoclimat.
- Zone étudiée : Paris.
- Station : Paris 6ème - Saint-Germain-des-Prés (000CT).
- Période étudiée : du 1er novembre 2023 au 31 octobre 2026.
- Données horaires valides : 24 600 observations.
- Données quotidiennes retenues : 1 018 journées.

Les données quotidiennes sont conservées lorsque la journée dispose d'au moins 20 observations horaires.

Une journée est considérée comme pluvieuse lorsque le cumul atteint au moins 1 mm de précipitations.

## Modèle de Machine Learning

Le modèle utilisé est une régression logistique développée avec scikit-learn.

La date est transformée en deux variables cycliques (sinus et cosinus), permettant de représenter la saisonnalité annuelle.

Le modèle utilise uniquement la date, sans température, humidité ou pression atmosphérique.

Les données sont séparées chronologiquement :

- Entraînement : 678 journées.
- Test : 340 journées.

## Évaluation du modèle

Sur les données de test :

| Indicateur | Modèle | Référence mensuelle |
|---|---:|---:|
| Accuracy (seuil 50 %) | 0,771 | 0,771 |
| ROC-AUC | 0,628 | 0,612 |
| Brier score | 0,180 | 0,180 |

Un test complémentaire a été réalisé avec un seuil de classification de 30 %.

| Indicateur | Modèle | Référence mensuelle |
|---|---:|---:|
| Accuracy | 0,506 | 0,403 |
| Précision | 0,279 | 0,259 |
| Rappel | 0,731 | 0,859 |
| F1-score | 0,404 | 0,398 |

Le seuil de 30 % a été étudié à titre exploratoire. Il n'a pas été retenu comme seuil optimal.

## Architecture technique

- SQLite : stockage des précipitations historiques.
- Python et pandas : collecte et préparation des données.
- scikit-learn : entraînement et évaluation du modèle.
- FastAPI : mise à disposition du modèle par une API.
- Streamlit : interface de consultation des estimations.

L'interface Streamlit interroge FastAPI, qui charge le modèle sauvegardé et calcule le résultat.

## Organisation des fichiers

- `collecte_donnees.py` : collecte des observations météorologiques.
- `entrainement_modele.py` : entraînement et évaluation.
- `encodage_date.py` : transformation cyclique des dates.
- `api.py` : API FastAPI.
- `interface.py` : interface Streamlit.
- `modele_pluie.pkl` : modèle entraîné.
- `requirements.txt` : dépendances Python.
- `.gitignore` : exclusions des fichiers locaux et confidentiels.

## Installation et lancement

Python doit être installé sur l'ordinateur.

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

Démarrer l'API FastAPI dans un premier terminal :

```bash
python -m uvicorn api:app --reload
```

Démarrer Streamlit dans un deuxième terminal :

```bash
python -m streamlit run interface.py
```

Ouvrir ensuite l'interface :

http://localhost:8501

La documentation interactive de l'API est accessible à l'adresse :

http://127.0.0.1:8000/docs

Le modèle sauvegardé permet de lancer l'API sans réentraîner le modèle.

## Données et confidentialité

La base de données SQLite utilisée pendant le développement n'est pas incluse dans ce dépôt.

La collecte complète et le réentraînement nécessitent les données historiques locales et l'accès à la source Infoclimat.

La clé API est conservée localement dans un fichier `.env`, exclu du dépôt GitHub.

## Limites du MVP

Le modèle estime une tendance statistique saisonnière et non une prévision météorologique quotidienne.

Ses performances restent limitées, notamment parce que la date est la seule variable explicative.

Il ne permet pas de prévoir précisément les épisodes de fortes pluies et ne doit pas être utilisé comme système d'alerte météorologique opérationnel.

## Perspectives d'amélioration

- Enrichir les données météorologiques.
- Étudier d'autres modèles de Machine Learning.
- Améliorer la validation des probabilités.
- Étendre l'étude à plusieurs stations météorologiques.
- Renforcer les tests techniques et l'accessibilité de l'interface.
```
