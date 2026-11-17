import sys

from PyQt6.QtWidgets import (
    QApplication,
)

from interface_gemini2 import FenetrePrincipale
from donnees import DataManager
from modele import ModeleBlockbuster

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger .csv
    data_manager = DataManager("movie_blockbusters.csv")
    donnees_clean = data_manager.donnees_clean

    # Créer et entraîner le modèle
    modele = ModeleBlockbuster(donnees_clean)
    score = modele.entrainer(donnees_clean[0], donnees_clean[1])

    print(f"F1-score :{score}")

    main_window = FenetrePrincipale(modele)

    main_window.show()
    app.exec()