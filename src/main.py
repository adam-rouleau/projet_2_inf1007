import sys

from PyQt6.QtWidgets import (
    QApplication,
)

from interface_gemini2 import FenetrePrincipale
from donnees import charger_donnees, preparer_donnees
from modele import ModeleBlockbuster

if __name__ == "__main__":
    app = QApplication(sys.argv)


    #charge le csv
    chemin = "movie_blockbusters.csv"
    df = charger_donnees(chemin)
    x, y = preparer_donnees(df)

    # Créer et entraîner le modèle
    modele = ModeleBlockbuster()
    score = modele.entrainer(x, y)

    print(f"F1-score :{score}")


    main_window = FenetrePrincipale(modele)
    # with open('src/style_interface.qss', "r") as f:
    #     style = f.read()
    #     main_window.setStyleSheet(style)

    main_window.show()
    app.exec()