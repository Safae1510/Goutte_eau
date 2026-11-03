
# Goutte d'Eau – MVP

## Présentation

Goutte d'Eau est un projet réalisé dans le cadre de mon Mastère en Transformation digitale et Intelligence artificielle.

L'objectif de ce MVP est d'estimer le risque statistique de pluie à Paris à partir d'une date choisie par l'utilisateur.

## Technologies utilisées

- Python : développement du projet
- Infoclimat : collecte des données météorologiques
- SQLite : stockage des précipitations
- scikit-learn : entraînement du modèle de Machine Learning
- FastAPI : création de l'API
- Streamlit : interface utilisateur

## Fonctionnement

Les données de précipitations ont été collectées pour une station météorologique située à Paris, sur une période de trois ans.

Après nettoyage, 1 018 journées ont été conservées pour entraîner et tester un modèle de régression logistique.

Le modèle utilise uniquement la date pour estimer le risque de pluie. Il est accessible via une API FastAPI.

L'interface Streamlit permet de sélectionner une date et d'afficher le pourcentage de risque estimé.

## Installation

Installer les bibliothèques nécessaires :

    python -m pip install -r requirements.txt

Démarrer l'API dans un premier terminal :

    python -m uvicorn api:app --reload

Démarrer l'interface dans un deuxième terminal :

    python -m streamlit run interface.py

L'application est ensuite accessible à l'adresse :

http://localhost:8501

## Fichiers du projet

- `collecte_donnees.py` : collecte des données
- `entrainement_modele.py` : entraînement et évaluation du modèle
- `encodage_date.py` : transformation des dates
- `api.py` : API FastAPI
- `interface.py` : interface Streamlit
- `modele_pluie.pkl` : modèle entraîné

Les données météorologiques proviennent d'Infoclimat, pour la station Paris 6ème - Saint-Germain-des-Prés (000CT).

La base SQLite `meteo_paris.db` est disponible dans le dépôt. Les conditions de réutilisation des données Infoclimat doivent être respectées.

La clé API Infoclimat n'est pas publiée. Le modèle sauvegardé permet de lancer l'application sans relancer la collecte ni l'entraînement.

## Limites

Le modèle repose uniquement sur les données historiques et la saisonnalité. Il fournit une estimation statistique du risque de pluie et non une prévision météorologique précise pour une journée donnée.

Ce MVP constitue une première version qui pourra être améliorée en intégrant d'autres données météorologiques.
