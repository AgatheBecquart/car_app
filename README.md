# Projet de prédiction de prix de vente de voitures

Ce projet consiste en l'analyse d'un jeu de données de vente de voitures avec leurs caractéristiques, ainsi que la création d'un modèle de machine learning permettant de prédire le prix de vente d'une voiture en fonction de ses caractéristiques.

## Technologies utilisées :

    Python 3
    Pandas pour la manipulation des données
    Scikit-learn pour la création et l'évaluation des modèles de machine learning
    FastAPI pour la création de l'API

## Installation

Clonez ce dépôt de code sur votre ordinateur :

    git clone https://github.com/votre-nom/projet-voitures.git

Installez les dépendances en exécutant la commande suivante :

    pip install -r requirements.txt


## Utilisation

### Analyse des données

Pour analyser les données de vente de voitures, exécutez le script car_analisis.ipynb. 

Ce script effectue les tâches suivantes :

    Lecture du jeu de données carprice.csv
    Nettoyage des données (suppression des doublons, des valeurs manquantes, etc.)
    Exploration des données (statistiques descriptives, visualisations)
    Transformation des données (encodage des variables catégorielles, standardisation des variables numériques)
    Division des données en ensembles d'entraînement et de test
    Enregistrement des données préparées dans des fichiers pour une utilisation ultérieure

### Création du modèle de machine learning

Pour créer et évaluer le modèle de machine learning, exécutez le script car_modelisation.ipynb. 

Ce script effectue les tâches suivantes :

    Chargement des données préparées
    Entraînement de plusieurs modèles de machine learning sur l'ensemble d'entraînement
    Évaluation des modèles sur l'ensemble de test
    Sélection du meilleur modèle
    Enregistrement du meilleur modèle dans un fichier pour une utilisation ultérieure

## Utilisation de l'API

Pour utiliser l'API de prédiction de prix de vente de voitures, exécutez la commande : 

    uvicorn main:app --reload 

Cette API permet de faire des prédictions de prix en envoyant des requêtes HTTP POST avec des données de caractéristiques de voiture au format JSON. 

Cette requête renverra une réponse JSON contenant la prédiction de prix de la voiture.
