import pandas as pd 


def charger_donnees(chemin : str):
    "charge les donnees du fichier csv"
    return pd.read_csv(chemin)

def preparer_donnees(df : pd.DataFrame):
    "Separer ce qu'on veut predire et avec quoi on le predit"

    X = df[["genre", "budget_usd", "rating", "runtime_min"]]
    y = df["blockbuster"]