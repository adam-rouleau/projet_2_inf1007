import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score


class ModeleBlockbuster(DecisionTreeClassifier):
class ModeleBlockbuster:

    def __init__(self):
        """Crée le modèle et prépare la conversion des genres."""

        preparation = ColumnTransformer([
            ("genre",
             OneHotEncoder(handle_unknown="ignore"),
             ["genre"])
        ], remainder="passthrough")

        self.modele = make_pipeline(
            preparation,
            DecisionTreeClassifier(
                max_depth=5,
                class_weight="balanced",
                random_state=42
            )
        )

    def entrainer(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Entraîne le modèle et retourne le F1-score."""

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        self.modele.fit(X_train, y_train)

        predictions = self.modele.predict(X_test)

        return float(f1_score(y_test, predictions))

    def predire(self, film: pd.DataFrame) -> int:
        """Retourne 1 pour blockbuster, sinon 0."""

        resultat = self.predict(film)

        return int(resultat[0])

  