
# Goutte d'Eau – MVP

## Présentation

Goutte d'Eau est un projet réalisé dans le cadre de mon Mastère en Transformation digitale et Intelligence artificielle.

L'objectif de ce MVP est d'estimer le risque statistique de pluie à Paris à partir d'une date sélectionnée par l'utilisateur.

## Technologies utilisées

- Python : développement du projet
- Infoclimat : collecte des données météorologiques
- SQLite : stockage des précipitations
- scikit-learn : entraînement du modèle de Machine Learning
- FastAPI : création de l'API
- Streamlit : interface utilisateur

## Fonctionnement

Les données de précipitations ont été collectées sur trois ans, pour la station Paris 6ème - Saint-Germain-des-Prés (000CT).

Après nettoyage, 1 018 journées ont été conservées pour entraîner et tester un modèle de régression logistique.

Le modèle utilise uniquement la date, transformée en deux variables représentant le cycle annuel.

L'interface Streamlit permet de choisir une date et d'afficher le pourcentage de risque calculé par le modèle via FastAPI.

## Installation et lancement

Python doit être installé sur l'ordinateur.

Créer et activer un environnement virtuel sur Mac :

    python3 -m venv .venv
    source .venv/bin/activate

Installer les bibliothèques :

    python -m pip install -r requirements.txt

Démarrer FastAPI dans un premier terminal :

    python -m uvicorn api:app --reload

Ouvrir un deuxième terminal, activer à nouveau l'environnement virtuel :

    source .venv/bin/activate

Puis lancer Streamlit :

    python -m streamlit run interface.py

L'interface est accessible à l'adresse :

http://localhost:8501

## Test de l'API

La documentation interactive de FastAPI est disponible à l'adresse :

http://127.0.0.1:8000/docs

Exemple de requête pour le 15 janvier 2027 :

http://127.0.0.1:8000/prediction?date_prevision=2027-01-15

Résultat obtenu :

    {
      "date": "2027-01-15",
      "station": "000CT",
      "risque_pluie_pourcentage": 35.3,
      "seuil_pluie_mm": 1.0
    }

## Résultats du modèle

Le modèle a été entraîné sur 678 journées et testé sur 340 journées.

Sur la période de test, son ROC-AUC est de 0,628, contre 0,612 pour une référence basée sur les fréquences mensuelles de pluie.

Un test complémentaire avec un seuil de classification de 30 % a donné un rappel de 73,1 % et un F1-score de 0,404.

Ces résultats montrent que le modèle identifie une tendance saisonnière, mais que ses capacités de prédiction restent limitées.

## Fichiers du projet

- `collecte_donnees.py` : collecte et préparation des données
- `entrainement_modele.py` : entraînement et évaluation du modèle
- `encodage_date.py` : transformation des dates
- `api.py` : API FastAPI
- `interface.py` : interface Streamlit
- `meteo_paris.db` : base de données SQLite
- `modele_pluie.pkl` : modèle entraîné
- `requirements.txt` : bibliothèques nécessaires
- `.env.example` : exemple de configuration de la clé API
- `.gitignore` : exclusion des fichiers locaux et confidentiels

## Source et collecte des données

Les données météorologiques proviennent d'Infoclimat, pour la station Paris 6ème - Saint-Germain-des-Prés (000CT).

La base SQLite utilisée pour le projet est disponible dans ce dépôt. La réutilisation des données doit respecter les conditions fixées par Infoclimat.

Pour relancer la collecte, il faut disposer d'une clé API Infoclimat.

Copier le fichier `.env.example` sous le nom `.env`, puis remplacer la valeur d'exemple par sa propre clé.

La collecte peut ensuite être lancée avec :

    python collecte_donnees.py

Et l'entraînement avec :

    python entrainement_modele.py

Ces opérations sont facultatives pour utiliser l'application, car la base et le modèle entraîné sont déjà fournis.

## Limites et améliorations possibles

Le modèle utilise uniquement la date et la saisonnalité. Il fournit une estimation statistique du risque de pluie, et non une prévision météorologique précise pour une journée donnée.

Les résultats ne doivent pas être utilisés comme des alertes météorologiques opérationnelles.

Une amélioration future pourrait notamment consister à utiliser les précipitations des jours précédents, afin de mieux tenir compte des conditions météorologiques récentes.
