import pandas as pd

import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline


class ModeleBlockbuster:

    def __init__(self):
        """
        Crée le modèle et prépare la conversion des genres.
        """
        self.pipeline = None

    def entrainer(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Entraîne le modèle et retourne le F1-score."""

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        preparation = ColumnTransformer([
            ("genre",
             OneHotEncoder(handle_unknown="ignore"),
             ["genre"])
        ], remainder="passthrough")


        pipeline = Pipeline([("preparation", preparation),("tree", DecisionTreeClassifier(random_state=42))])

        param_grid = {
            "tree__max_depth": [4, 5, 6, None],
            'tree__class_weight': [
                None, 
                'balanced', 
                {0: 1, 1: 4},
                {0: 1, 1: 5},
                {0: 1, 1: 10},
            ]
        }

        self.recherchegrille = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            scoring='f1',
            cv=5,
            n_jobs=-1
        )

        self.recherchegrille.fit(X_train, y_train)

        predictions = self.recherchegrille.predict(X_test)

        ConfusionMatrixDisplay.from_estimator(self.recherchegrille, X_test, y_test)
        plt.show()

        print("Best parameters:", self.recherchegrille.best_params_)
        print("Best mean CV F1:", self.recherchegrille.best_score_)
        return float(f1_score(y_test, predictions))

    def predire(self, film: pd.DataFrame) -> int:
        """Retourne 1 pour blockbuster, sinon 0."""

        resultat = self.recherchegrille.predict(film)

        return int(resultat[0])

  