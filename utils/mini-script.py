import json
from pathlib import Path

import pandas as pd


dossier = Path(__file__).parent
donnees = pd.read_csv(dossier / "movie_blockbusters.csv")
colonnes_numeriques = donnees.select_dtypes(include="number")

resultats = {}

for colonne in colonnes_numeriques.columns:
    minimum = colonnes_numeriques[colonne].min().item()
    maximum = colonnes_numeriques[colonne].max().item()

    resultats[colonne] = {"minimum": minimum, "maximum": maximum}
    print(f"{colonne} : minimum = {minimum}, maximum = {maximum}")

fichier_json = dossier / "movie_blockbusters_min_max.json"
with fichier_json.open("w", encoding="utf-8") as fichier:
    json.dump(resultats, fichier, indent=4, ensure_ascii=False)

print(f"\nRésultats exportés vers {fichier_json.name}")