import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline

def charger_donnees(chemin : str):
    "charge les donnees du fichier csv"
    return pd.read_csv(chemin)

def preparer_donnees(df : pd.DataFrame):
    "Separer ce qu'on veut predire et avec quoi on le predit"

    x = df[["genre", "budget_usd", "rating", "runtime_min"]]
    y = df["blockbuster"]

    return x, y 

class ModeleBlockbuster:

    def __init__(self):
        """
        Crée le modèle et prépare la conversion des genres.
        """
        self.recherchegrille = None
        self.meilleur_seuil_ = 0.5

    def entrainer(self, X: pd.DataFrame, y: pd.Series) -> float:
        """
        Entraîne le modèle et retourne le F1-score.
        """

        X_train, X_test, y_train, y_test = train_test_split(
            X_train_val, y_train_val,
            test_size=0.2,
            random_state=42,
            stratify=y_train_val
        )

        preparation = ColumnTransformer([
            ("genre",
             OneHotEncoder(handle_unknown="ignore"),
             ["genre"])
        ], remainder="passthrough")


        pipeline = Pipeline([("preparation", preparation),("rf", RandomForestClassifier(random_state=42, n_jobs=-1))])

        param_grid = {
            "rf__n_estimators": [100, 200], 
            "rf__max_depth": [6, 10, 15, None],
            "rf__min_samples_split": [2, 5, 10],
            "rf__class_weight": ['balanced', 'balanced_subsample', None]
        }

        self.recherchegrille = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            scoring='f1',
            cv=5,
            n_jobs=-1
        )

        self.recherchegrille.fit(X_train, y_train)

        # Probabilité d'être blockbuster
        probas_test = self.recherchegrille.predict_proba(X_test)[:, 1]

        seuils = np.linspace(0.01, 0.99, 100)
        self.meilleur_seuil_ = 0.5 #default
        meilleur_f1 = 0.0 #plus pas comme ça quand augmente on a toujours mieux 

        for seuil in seuils:
            predictions_seuil = (probas_test >= seuil).astype(int)
            score = f1_score(y_train, predictions_seuil)
            if score > meilleur_f1:
                meilleur_f1 = score 
                meilleur_seuil = seuil

        self.meilleur_seuil_ = meilleur_seuil
        print("Meilleur seuil: ", self.meilleur_seuil_)
        print("Meilleur F1: ", meilleur_f1)

        predictions_optimales = (probas_test >= self.meilleur_seuil_).astype(int)

        ConfusionMatrixDisplay.from_predictions(y_test, predictions_optimales)
        plt.show()

        print("Best parameters:", self.recherchegrille.best_params_)
        print("Best mean CV F1:", self.recherchegrille.best_score_)
        return float(f1_score(y_test, predictions_optimales))

    def predire(self, film: pd.DataFrame) -> int:
        """Retourne 1 pour blockbuster, sinon 0."""

        print("Shape film: ", film.shape)
        print("Film: ", film)

        # Probabilité classe 1
        probas = self.recherchegrille.predict_proba(film)[:, 1]
        
        seuil = self.meilleur_seuil_
        print(seuil)
        
        resultat = (probas >= seuil).astype(int)
        return int(resultat[0])

(x, y) = preparer_donnees(charger_donnees("movie_blockbusters.csv"))
modele = ModeleBlockbuster()
modele.entrainer(x, y)

film = pd.DataFrame([{
    "genre": "Comedy",
    "budget_usd": 50000000,
    "rating": 10,
    "runtime_min": 120
}])

print(modele.predire(film))