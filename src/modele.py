import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score


class ModeleBlockbuster(DecisionTreeClassifier):

    def __init__(self):
        """
        Contructeur de ModeleBlockbuster, héritant de DecisionTreeClassifier
        """
        super().__init__(
            max_depth=5, 
            random_state=42
        )

    def entrainer(self, X:pd.DataFrame, y:pd.Series):
        """
        Entraîne le modèle et retourne son F1-score.
        """

        # Transformer le genre en colonnes numériques
        X = pd.get_dummies(X, columns=["genre"])

        # Séparer les données en entraînement et test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        # Entraîner le modèle
        self.fit(X_train, y_train)

        # Tester le modèle
        predictions = self.predict(X_test)

        # Calculer le score
        score = f1_score(y_test, predictions)

        return score

    def predire(self, film: pd.DataFrame) -> int:
        """
        Prédit si un film est un blockbuster.
        """

        resultat = self.predict(film)

        return int(resultat[0])
  