# Prédiction du succès commercial d'un film

Projet 2 « De la donnée à l'application » — INF1007, Polytechnique Montréal.

**Auteurs : Adam Rouleau et Eliott Magnet Da Costa.**

## Présentation

L'oracle du box office est une application qui estime si un film appartient à la catégorie des blockbusters à partir de ses caractéristiques. L'utilisateur renseigne les informations demandées dans une interface graphique, lance une prédiction, peut consulte une matrice de confusion et retrouve les prédictions précédentes dans un historique.

La cible `blockbuster` vaut 1 lorsque les recettes dépassent trois fois le budget et 100 millions USD, et 0 sinon. Il s'agit d'une estimation statistique et non d'une garantie de rentabilité.

## Jeu de données

- Source : [What Makes a Movie a Blockbuster? 5,000 Films — vedauv, Kaggle](https://www.kaggle.com/datasets/vedauv/what-makes-a-movie-a-blockbuster-5000-films).
- Format : CSV ; jeu d'origine de 5 000 films
- Columns du fichier csv :

Column	                Description
movie_id	            Unique identifier
title	                Synthetic movie title (placeholder)
year	                Release year (1980–2024)
decade	                Decade label (1980s, 1990s, etc.)
genre	                Primary genre
runtime_min	            Runtime in minutes
budget_usd	            Production budget (USD)
revenue_usd	            Box office revenue (USD)
profit_usd	            Revenue minus budget (USD)
roi	                    Return on investment
rating	                Average rating (0–10)
vote_count	            Number of votes
popularity	            Popularity score
blockbuster	            Target: 1 if hit, 0 otherwise

- Les colonnes de recettes, profit et ROI ne doivent pas servir de prédicteurs puisqu'elles révèlent directement ou indirectement la cible.
- Licence : CC0 Public Domain 

## Installation et lancement

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

Bibliothèques utilisées dans les versions examinées : PyQt6, pandas, NumPy, scikit-learn, Matplotlib et joblib. Vérifier que le fichier `requirements.txt`

Lancer l'application :

```bash
python main.py
```

## Fonctionnement 


 `main.py`                             Point d'entrée de l'application. 
 `src/donnees.py`                      Chargement et préparation des données avec pandas. 
 `src/modele.py`                       Entraînement, évaluation, prédiction et gestion du modèle. 
 `interface.py`                        Gestion de l'interface, dialogue, historique, graphique  

Le modèle est sauvegardé avec joblib : un modèle déjà enregistré est réutilisé et il faut supprimer le fichier joblib pour un nouvel entraînement. 

## Modèle et résultats

Le modèle développé repose sur une forêt aléatoire (`RandomForestClassifier`) de scikit-learn, qui combine plusieurs arbres de décision. Le prétraitement permet notamment de convertir les variables catégorielles avec `OneHotEncoder`. La recherche d'hyperparamètres avec `GridSearchCV` utilise le F1-score. Les données sont séparées en entraînement (60 %), validation (20 %) et test (20 %), avec stratification et graine fixée à 42. La grille compare 72 configurations avec une validation croisée à cinq plis. Après entraînement, 100 seuils entre 0,01 et 0,99 sont évalués sur la validation ; le meilleur est appliqué au test et aux nouvelles prédictions. Les comparaisons vectorisées NumPy convertissent les probabilités en classes. La matrice affiche les effectifs et les pourcentages par vraie catégorie.

Le F1-score est choisi pour tenir compte à la fois de la précision et du rappel de la classe blockbuster, minoritaire. La matrice de confusion permet de visualiser les bonnes classifications et les erreurs.

Le modèle reste limité par les caractéristiques disponibles et le caractère synthétique du jeu de données. Les estimations ne constituent pas des probabilités de succès commercial garanties dans le monde réel.

## Outil du chapitre 7

Nous utilisons les décorateurs intégrés `@property` et `@...setter`. Dans `src/donnees.py`, ils permettent notamment de lire les données brutes et de charger un CSV lors de l'affectation à `donnees_brutes`. Dans `src/modele.py`, ils encadrent notamment l'accès au seuil, à la grille et à la matrice de confusion. Par exemple, le setter `matrice_confusion` calcule la matrice à partir des vraies classes, des prédictions et des labels.

## Références techniques

- [Python — JSON](https://docs.python.org/3/library/json.html), [gestion des chemins](https://docs.python.org/3/library/os.path.html), [exceptions](https://docs.python.org/3/tutorial/errors.html).
- [pandas — documentation](https://pandas.pydata.org/docs/).
- [scikit-learn — arbres de décision](https://scikit-learn.org/stable/modules/tree.html), [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html), [F1-score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html), [matrice de confusion](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html).
- [PyQt6 — documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/), [Matplotlib — documentation](https://matplotlib.org/stable/), [NumPy — documentation](https://numpy.org/doc/stable/).
- [joblib — persistance](https://joblib.readthedocs.io/en/latest/persistence.html), [pytest](https://docs.pytest.org/), [GitHub Actions](https://docs.github.com/en/actions).

