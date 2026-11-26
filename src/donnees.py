from pathlib import Path

import pandas as pd 

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


class DataManager():
    """
    Gestionnaire du chargement et de la préparation de la base de données.

    Note: Les propriétés utilisent les décorateurs de Python, 
    ce n'est pas la méthode la plus lisible mais ça m'a fait de la bonne pratique pour l'exam.
    - Adam
    """

    def __init__(self, chemin:str):
        self.__donnees_brutes: pd.DataFrame | None = None
        self.donnees_brutes = chemin # Setter directement appelé

    @property
    def donnees_brutes(self) -> pd.DataFrame:
        """
        Retourne données brutes si chargées.
        """
        if self.__donnees_brutes is None:
            raise ValueError("Aucune donnée chargée")
        else:
            return self.__donnees_brutes

    @donnees_brutes.setter
    def donnees_brutes(self, chemin:str):
        """
        Charge les données du CSV.
        """
        self.__donnees_brutes = pd.read_csv(chemin)

    @property
    def donnees_clean(self) -> tuple[pd.DataFrame, pd.Series]:
        """
        Séparer x (entrées) et y (blockbuster ou non).
        """
        df = self.donnees_brutes
        x = df[["genre", "budget_usd", "rating", "runtime_min"]].copy()
        y = df["blockbuster"].copy()
        return x, y

    @property 
    def donnees_traitees(self) -> ColumnTransformer:
        """
        Retourne les données traitées avec OneHotEncoder
        """
        return ColumnTransformer([
            ("genre", OneHotEncoder(handle_unknown="ignore"), ["genre"])
        ], remainder="passthrough")

# Tests 
if __name__ == "__main__":
    csv_path = Path(__file__).resolve().parent.parent / "movie_blockbusters.csv"
    datamanager = DataManager(str(csv_path))
    donnees_clean = datamanager.donnees_clean

    # Faire le head et to_string permet d'afficher le contenu des 10 premières lignes au lieu de seulement afficher l'indice
    print("-------")
    print(f"5 premières lignes de x:\n{donnees_clean[0].head(5).to_string()}\n")
    print(f"5 premières lignes de y:\n{donnees_clean[1].head(5)}")
    print("-------")