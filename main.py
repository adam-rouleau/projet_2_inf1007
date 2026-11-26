import sys 
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
)

from src.interface import FenetrePrincipale
from src.donnees import DataManager 
from src.modele import ModeleBlockbuster

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger .csv
    csv_path = Path(__file__).resolve().parent / "movie_blockbusters.csv"
    data_manager = DataManager(str(csv_path))

    # Création et entraînement du modèle
    modele = ModeleBlockbuster(data_manager)
    if not modele.charger_modele():
        print("veuillez patienter durant l'entraînement.")
        score = modele.entrainer(data_manager.donnees_clean[0], data_manager.donnees_clean[1])
        print(f"F1-score :{score}")
    else:
        print("Modèle chargé.")

    main_window = FenetrePrincipale(modele)

    main_window.show()
    app.exec()