import pandas as pd 

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


class DataManager():
    """
    Classe contenant les fonctions de gestion des données.

    Note: Les propriétés utilisent les décorateurs de Python, 
    ce n'est pas la méthdode la plus lisible mais ça m'a fait de la bonne pratique pour l'exam.
    - Adam
    """
    def __init__(self, chemin:str):
        self.__donnees_brutes: pd.DataFrame | None = None
        self.donnees_brutes = chemin        

    @property
    def donnees_brutes(self) -> pd.DataFrame:
        """Retourne données brutes si chargées."""
        if self.__donnees_brutes is None:
            raise ValueError("Aucune données chargées")
        else:
            return self.__donnees_brutes

    @donnees_brutes.setter
    def donnees_brutes(self, chemin:str) -> pd.DataFrame:
        """Charge les données du CSV."""
        return pd.read_csv(chemin)

    @property
    def donnees_clean(self) -> tuple[pd.DataFrame, pd.Series]:
        """Séparer x et y."""
        df = self.donnees_brutes
        x = df[["genre", "budget_usd", "rating", "runtime_min"]].copy()
        y = df["blockbuster"].copy()
        return x, y

    @property 
    def donnees_traitees(self) -> ColumnTransformer:
        """Retourne les données traitées avec OneHotEncoder"""
        return ColumnTransformer([
            ("genre", OneHotEncoder(handle_unknown="ignore"), ["genre"])
        ], remainder="passthrough")