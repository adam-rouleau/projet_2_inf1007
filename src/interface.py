from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (  
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QDialog,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

import pandas as pd 
from datetime import datetime 
from pathlib import Path
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

try:
    from .modele import ModeleBlockbuster
    from .utils.verification_valeurs import (
        VerificateurGenre,
        VerificateurRating,
        VerificateurBudget,
        VerificateurRuntime,
    )
    from .utils.dialogue import Dialogue
except ImportError:
    from modele import ModeleBlockbuster
    from utils.verification_valeurs import (
        VerificateurGenre,
        VerificateurRating,
        VerificateurBudget,
        VerificateurRuntime,
    )
    from utils.dialogue import Dialogue

class FenetrePrincipale(QMainWindow):
    """
    Création de la fenêtre principale.

    Hérite de QMainWindow.
    """
    def __init__(self, modele:ModeleBlockbuster):
        super().__init__()
        self.modele = modele 

        self.setObjectName("fenetre_principale")
        self.setWindowTitle("Prédicteur de Blockbuster")
        self.setMinimumWidth(510)

        chemin_qss = Path(__file__).resolve().with_name("style_interface.qss")
        if chemin_qss.exists():
            self.setStyleSheet(chemin_qss.read_text(encoding="utf-8"))

        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        self.__layout_principal = QVBoxLayout()
        self.setCentralWidget(widget_principal)

        self.__layout_principal = QVBoxLayout()
        self.__layout_principal.setContentsMargins(35, 35, 35, 35)
        self.__layout_principal.setSpacing(20)
        widget_principal.setLayout(self.__layout_principal)

        # En-tête / Titre Principal avec un style "Cinéma"
        titre_application = QLabel("L'oracle du Box-Office")
        titre_application.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre_application.setObjectName("titre")
        self.__layout_principal.addWidget(titre_application)

        # Description Principale
        sous_titre_application = QLabel("Entrez les données d'un film et découvrez s'il remportera le box-office !\n Succès validé si le revenu atteint 3x le budget et dépasse 100M$.")
        sous_titre_application.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sous_titre_application.setWordWrap(True)
        sous_titre_application.setObjectName("sous_titre")
        self.__layout_principal.addWidget(sous_titre_application)

        # Conteneur "Carte" pour les inputs pour un effet moins stérile
        carte_form = QFrame()
        carte_form.setObjectName("carte_form")
        layout_carte = QVBoxLayout(carte_form)
        layout_carte.setContentsMargins(25, 25, 25, 25)
        layout_carte.setSpacing(15)
        self.__layout_principal.addWidget(carte_form)

        # Genre
        label_question_comedie = QLabel("Genre du film")
        label_question_comedie.setObjectName("label_form")
        layout_carte.addWidget(label_question_comedie)
        
        self.question_genre = QComboBox()
        self.question_genre.addItems(["Sélectionnez un genre",
                                      "Comedy", 
                                      "Sci-Fi", 
                                      "Horror", 
                                      "Documentary", 
                                      "Action", 
                                      "Thriller", 
                                      "Romance", 
                                      ])
        layout_carte.addWidget(self.question_genre)

        # Formulaires restants
        self.question_budget = self.ajouter_form("Budget (USD) - Entre X et X2", layout_carte, "Ex: 50000000")

        self.question_rating = self.ajouter_form("Note (Rating)", layout_carte, "Ex: 7.5")

        self.question_runtime = self.ajouter_form("Durée (Runtime en minutes)", layout_carte, "Ex: 120")

        self.probleme_question = QLabel("Veuillez répondre à toutes les questions")
        self.probleme_question.setObjectName("label_erreur")
        self.probleme_question.setVisible(False)
        layout_carte.addWidget(self.probleme_question)

        # Layout Boutons
        layout_boutons = QHBoxLayout()
        layout_boutons.setSpacing(15)
        self.__layout_principal.addLayout(layout_boutons)

        self.bouton_predire = QPushButton("Lancer la prédiction")
        self.bouton_predire.setObjectName("bouton_principal")
        self.bouton_predire.clicked.connect(self.predire)
        layout_boutons.addWidget(self.bouton_predire)

        self.bouton_generer_graphique = QPushButton("Générer Graphique")
        self.bouton_generer_graphique.setObjectName("bouton_secondaire")
        self.bouton_generer_graphique.clicked.connect(self.generer_graphique)
        layout_boutons.addWidget(self.bouton_generer_graphique)

        self.bouton_historique = QPushButton("Afficher l'historique")
        self.bouton_historique.setObjectName("bouton_secondaire")
        self.bouton_historique.clicked.connect(self.afficher_historique)
        layout_boutons.addWidget(self.bouton_historique)

    def ajouter_form(self, question: str, layout: QVBoxLayout, placeholder: str = "") -> QLineEdit:
        '''
        La fonction ajouter_form prend une question et ajoute automatiquement un form adapté.

        Entrée: question posée, layout dans lequel le form est inséré
        Retourne: l'objet QLineEdit créé
        '''
        label_question = QLabel(question)
        label_question.setObjectName("label_form")
        layout.addWidget(label_question)
        
        plage_question = QLineEdit()
        plage_question.setPlaceholderText(placeholder)
        layout.addWidget(plage_question)

        return plage_question

    def predire(self):
        '''
        Prédire est la fonction actionnée quand le bouton 'prédire' est pressé. 

        Entrée: self (fenêtre principale)
        Retourne: True / False
        '''
        valeur_reponse_genre = self.question_genre.currentText()
        if not VerificateurGenre().verification(valeur_reponse_genre):
            return

        # Vérification valeur Rating
        valeur_reponse_score = float( self.question_rating.text())
        if not VerificateurRating().verification(valeur_reponse_score):
            return
        valeur_reponse_score = float(valeur_reponse_score)

        # Vérification réponse budget
        valeur_reponse_budget = int(self.question_budget.text())
        if not VerificateurBudget().verification(valeur_reponse_budget):
            return
        valeur_reponse_budget = float(valeur_reponse_budget)

        # Vérification réponse runtime
        valeur_reponse_runtime = float(self.question_runtime.text())
        if not VerificateurRuntime().verification(valeur_reponse_runtime):
            return
        valeur_reponse_runtime = float(valeur_reponse_runtime)

        # Créer le tableau du film
        film = pd.DataFrame([{
            "genre": valeur_reponse_genre,
            "budget_usd": valeur_reponse_budget,
            "rating": valeur_reponse_score,
            "runtime_min": valeur_reponse_runtime
        }])
        
        # Faire la prédiction
        resultat = self.modele.predire(film)

        prediction = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "genre": valeur_reponse_genre,
        "budget_usd": valeur_reponse_budget,
        "rating": valeur_reponse_score,
        "runtime_min": valeur_reponse_runtime,
        "blockbuster": int(resultat)
        }

        try:
            self.modele.enregistrer_prediction(prediction, film)
        except (OSError, ValueError, TypeError) as erreur:
            Dialogue(f"Prédiction calculée, mais historique non enregistré : {erreur}", "OK").activation()

        
        # Afficher le résultat
        if resultat == 1:
            message = "Blockbuster prédit !"
        else:
            message = "Le film est prédit comme non-blockbuster."
        
        Dialogue(message, "OK" ).activation()

    def generer_graphique(self):
        """Affiche une matrice de confusion"""
        matrice = self.modele.matrice_confusion
        if matrice is None:
            Dialogue("Le modèle doit d'abord être entraîné.", "OK").activation()
            return

        fenetre = QDialog(self)
        fenetre.setWindowTitle("Évaluation du modèle : matrice de confusion")
        largeur = self.width()
        hauteur = self.height()
        fenetre.setFixedSize(largeur, hauteur)
        layout = QVBoxLayout(fenetre)

        figure = Figure(figsize=(5, 4), tight_layout=True)
        axe = figure.add_subplot(111)
        image = axe.imshow(matrice, cmap="Blues")
        figure.colorbar(image, ax=axe, label="Nombre de films")
        axe.set_title(f"Résultats sur le jeu de test (seuil : {self.modele.meilleur_seuil:.2f})")
        axe.set_xlabel("Catégorie prédite")
        axe.set_ylabel("Vraie catégorie")
        axe.set_xticks([0, 1], ["Non-blockbuster", "Blockbuster"])
        axe.set_yticks([0, 1], ["Non-blockbuster", "Blockbuster"])
        axe.set_aspect("equal")

        for i in range(2):
            for j in range(2):
                couleur = "white" if matrice[i, j] > matrice.max() / 2 else "black"
                total_reel = matrice[i].sum()
                pourcentage = matrice[i, j] / total_reel * 100 if total_reel else 0
                axe.text(
                    j, i, f"{matrice[i, j]}\n({pourcentage:.1f} %)",
                    ha="center", va="center", color=couleur, fontsize=12
                )

        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
        layout.addWidget(QLabel(
            "La diagonale représente les bonnes prédictions; les autres cases, les erreurs. "
            "Les pourcentages sont calculés par vraie catégorie."
        ))
        bouton_fermer = QPushButton("Fermer")
        bouton_fermer.clicked.connect(fenetre.accept)
        layout.addWidget(bouton_fermer)
        fenetre.exec()

    def afficher_historique(self) -> None:
        """Affiche les prédictions passées dans un tableau ."""
        try:
            predictions = self.modele.lire_historique()
        except (OSError, ValueError) as erreur:
            Dialogue(f"Impossible de lire l'historique : {erreur}", "OK").activation()
            return

        fenetre = QDialog(self)
        fenetre.setObjectName("dialogue_historique")
        fenetre.setWindowTitle("Historique des prédictions")
        largeur = self.width()
        hauteur = self.height()
        fenetre.setFixedSize(largeur, hauteur)
        layout = QVBoxLayout(fenetre)
        layout.addWidget(QLabel(f"Nombre de prédictions enregistrées : {len(predictions)}"))
        tableau = QTableWidget(len(predictions), 6)
        tableau.setHorizontalHeaderLabels([
            "Date", "Genre", "Budget ($)", "Note", "Durée (min)", "Prédiction"
        ])
        en_tetes = tableau.horizontalHeader()
        if en_tetes is not None:
            en_tetes.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tableau.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tableau.setAlternatingRowColors(True)

        for numero, prediction in enumerate(reversed(predictions)):
            valeurs = [
                prediction.get("date", ""),
                prediction.get("genre", ""),
                str(prediction.get("budget_usd", "")),
                str(prediction.get("rating", "")),
                str(prediction.get("runtime_min", "")),
                "Blockbuster" if prediction.get("blockbuster", prediction.get("blockbuster_predit")) == 1
                else "Non-blockbuster",
            ]
            for colonne, valeur in enumerate(valeurs):
                tableau.setItem(numero, colonne, QTableWidgetItem(valeur))

        layout.addWidget(tableau)
        bouton_fermer = QPushButton("Fermer")
        bouton_fermer.clicked.connect(fenetre.accept)
        layout.addWidget(bouton_fermer)
        fenetre.exec()