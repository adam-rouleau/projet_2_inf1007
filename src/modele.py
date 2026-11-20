import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import os
import json
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, confusion_matrix

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import f1_score, ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


class ModeleBlockbuster:
    def __init__(self, donnees_clean:tuple[pd.DataFrame, pd.Series]):
        """
        Crée le modèle et prépare la conversion des genres.
        """
        self.pipeline = None
        self.matrice_confusion = None
        self.chemin_historique = "historique.json"
        self.donnees_clean = donnees_clean
        self.recherchegrille: GridSearchCV | None = None
        self.meilleur_seuil_ = 0.5
        self.colonnes_entree_ = None

    @property
    def grille_parametres(self) -> dict:
        "Grille des paramètres et des valeurs essayées par GridSearchCV"
        return {
                    "rf__n_estimators": [100, 200], 
                    "rf__max_depth": [6, 10, 15, None],
                    "rf__min_samples_split": [2, 5, 10],
                    "rf__class_weight": ['balanced', 'balanced_subsample', None]
                }

    @property 
    def pipeline(self) -> Pipeline:
        """Préparation données + RandomForest"""
        preparation = ColumnTransformer([
            ("genre", OneHotEncoder(handle_unknown="ignore"), ["genre"])
        ], remainder="passthrough")
        return Pipeline([
            ("preparation", preparation),
            ("rf", RandomForestClassifier(random_state=42, n_jobs=-1))
        ])

    def _valider_colonnes(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        S'assure que les colonnes sont dans le bon ordre.

        NOTE: Le code vient de Github Copilot - Basically inutile dans 
        NOTRE programme mais super utile parce que si les colonnes sont
        dans le mauvais ordre somehow, Scikit est super sensible et 
        fait une mauvasie prédiction. 
        """
        if self.colonnes_entree_ is None:
            return X

        return X.reindex(columns=self.colonnes_entree_)

    def entrainer(self, X: pd.DataFrame, y: pd.Series) -> float:
        """
        Entraîne le modèle et retourne le F1-score.

        NOTE: Avant on séparait avec train_test_split 1 fois,
        maintenant on le fait une première fois pour faire les données
        d'entraînement, et une deuxième fois pour séparer validation 
        et le test.
        """
        self.colonnes_entree_ = list(X.columns)

        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y,
            test_size=0.4,
            random_state=42,
            stratify=y
        )

        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp,
            test_size=0.5,
            random_state=42,
            stratify=y_temp
        )

        self.recherchegrille = GridSearchCV(
            estimator = self.pipeline,
            param_grid = self.grille_parametres,
            scoring = 'f1',
            cv = 5,
            n_jobs = -1
        )

        # Entraînement
        self.recherchegrille.fit(X_train, y_train)

        # Recherche meilleur seuil (données de validation utilisées)
        probas_val = self.recherchegrille.predict_proba(X_val)[:, 1]

        seuils = np.linspace(0.01, 0.99, 100)
        meilleur_f1 = 0.0 # plus bas comme ça quand augmente on a toujours mieux 
        meilleur_seuil = 0.5 # on commence au milieu

        self.matrice_confusion = confusion_matrix(y_test, predictions, labels=[0, 1])
        # Trouver le meilleur seuil
        for seuil in seuils:
            predictions_seuil = (probas_val >= seuil).astype(int)
            score = f1_score(y_val, predictions_seuil)
            if score > meilleur_f1:
                meilleur_f1 = score 
                meilleur_seuil = seuil

        self.meilleur_seuil_ = meilleur_seuil

        print("Meilleur seuil: ", self.meilleur_seuil_)
        print("Meilleur F1 (sur les données de validation): ", meilleur_f1)

        # Évaluation sur données de tests (on vérifie que c'était pas un fluke)
        probas_test = self.recherchegrille.predict_proba(X_test)[:, 1]
        predictions_test = (probas_test >= self.meilleur_seuil_).astype(int)
        score_final = f1_score(y_test, predictions_test) # Le score F1 obtenu sur le jeu de test

        ConfusionMatrixDisplay.from_predictions(y_test, predictions_test)
        plt.show()

        print("Best parameters:", self.recherchegrille.best_params_)
        print("Best mean CV F1:", self.recherchegrille.best_score_)
        print("F1 score final (sur données de test)", score_final)

        return float(score_final)

    def predire(self, film: pd.DataFrame) -> int:
        """Retourne 1 pour blockbuster, sinon 0."""
        film = self._valider_colonnes(film)


        print("Shape film: ", film.shape)
        print("Film: ", film)

        if self.recherchegrille is None:
            raise ValueError("Le modèle n'a pas encore été entraîné.")

        return int(resultat[0])

    def lire_historique(self):
        if not os.path.exists(self.chemin_historique):
            return []

        with open(self.chemin_historique, "r", encoding="utf-8") as fichier:
            try:
                historique = json.load(fichier)
            except json.JSONDecodeError as erreur:
                raise ValueError("Le fichier historique.json est invalide") from erreur
        if not isinstance(historique, list):
            raise ValueError("L'historique doit contenir une liste")
        return historique

    def enregistrer_prediction(self, prediction):
        historique = self.lire_historique()

        historique.append(prediction)

        with open(self.chemin_historique, "w", encoding="utf-8") as fichier:
            json.dump(historique, fichier, indent=4)
        # Probabilité classe 1
        probas = self.recherchegrille.predict_proba(film)[:, 1]
        
        seuil = self.meilleur_seuil_
        print(seuil)
        
        resultat = (probas >= seuil).astype(int)
        return int(resultat[0])
