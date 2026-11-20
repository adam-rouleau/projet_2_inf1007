import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PyQt6.QtWidgets import QApplication

from interface_gemini2 import FenetrePrincipale


class FauxModele:
    def __init__(self, resultat):
        self.resultat = resultat
        self.film_recu = None

    def predire(self, film):
        self.film_recu = film
        return self.resultat


def test_prediction_is_shown_in_the_main_window():
    app = QApplication.instance() or QApplication([])
    modele = FauxModele(1)
    fenetre = FenetrePrincipale(modele)
    fenetre.question_genre.setCurrentText("Comedy")
    fenetre.question_budget.setText("50000000")
    fenetre.question_rating.setText("7.5")
    fenetre.question_runtime.setText("120")
    fenetre.show()

    fenetre.predire()
    app.processEvents()

    assert fenetre.resultat_prediction.text() == "Blockbuster prédit !"
    assert fenetre.resultat_prediction.isVisible()
    assert modele.film_recu.iloc[0]["genre"] == "Comedy"
    fenetre.close()


def test_invalid_input_shows_error_without_running_prediction():
    app = QApplication.instance() or QApplication([])
    modele = FauxModele(1)
    fenetre = FenetrePrincipale(modele)
    fenetre.question_genre.setCurrentText("Comedy")
    fenetre.question_budget.setText("invalid")
    fenetre.question_rating.setText("7.5")
    fenetre.question_runtime.setText("120")

    fenetre.predire()

    assert "budget" in fenetre.resultat_prediction.text().lower()
    assert modele.film_recu is None
    fenetre.close()
