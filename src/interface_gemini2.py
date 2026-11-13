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
)

from exceptions import (
    ErreurInputBudgetFilm, 
    ErreurInputLongueurFilm
)

import pandas as pd

class FenetrePrincipale(QMainWindow):
    '''
    FenetrePrincipale crée la fenêtre principale. 
    
    Hérite de: QMainWindow
    '''
    def __init__(self, modele):
        super().__init__()
        self.modele = modele

        self.setWindowTitle("CinePredict - Prédicteur de succès au Box Office")
        self.setMinimumWidth(520)
        
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        self.__layout_principal = QVBoxLayout()
        self.__layout_principal.setContentsMargins(35, 35, 35, 35)
        self.__layout_principal.setSpacing(20)
        widget_principal.setLayout(self.__layout_principal)

        # En-tête / Titre Principal avec un style "Cinéma"
        titre_application = QLabel("🎬 Box Office Oracle")
        titre_application.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre_application.setObjectName("titre")
        self.__layout_principal.addWidget(titre_application)

        # Description Principale
        sous_titre_application = QLabel("Entrez les données d'un film et découvrez s'il remportera le box-office !\n💡 Succès validé si le revenu atteint 3x le budget et dépasse 100M$.")
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
        self.question_budget.textChanged.connect(self.on_text_changed)

        self.question_rating = self.ajouter_form("Note (Rating)", layout_carte, "Ex: 7.5")
        self.question_rating.textChanged.connect(self.on_text_changed)

        self.question_runtime = self.ajouter_form("Durée (Runtime en minutes)", layout_carte, "Ex: 120")
        self.question_runtime.textChanged.connect(self.on_text_changed)

        self.probleme_question = QLabel("Veuillez répondre à toutes les questions")
        self.probleme_question.setObjectName("label_erreur")
        self.probleme_question.setVisible(False)
        layout_carte.addWidget(self.probleme_question)

        # Layout Boutons
        layout_boutons = QHBoxLayout()
        layout_boutons.setSpacing(15)
        self.__layout_principal.addLayout(layout_boutons)

        self.bouton_predire = QPushButton("✨ Lancer la prédiction")
        self.bouton_predire.setObjectName("bouton_principal")
        self.bouton_predire.clicked.connect(self.predire)
        layout_boutons.addWidget(self.bouton_predire)

        self.bouton_generer_graphique = QPushButton("📊 Générer Graphique")
        self.bouton_generer_graphique.setObjectName("bouton_secondaire")
        self.bouton_generer_graphique.clicked.connect(self.generer_graphique)
        layout_boutons.addWidget(self.bouton_generer_graphique)

        # Application du style global (QSS) pour une ambiance chaleureuse et cinématographique
        self.appliquer_styles()

    def appliquer_styles(self):
        style_feuille = """
            QMainWindow {
                background-color: #12141c;
            }
            QLabel#titre {
                font-size: 26px;
                font-weight: bold;
                color: #f1f2f6;
                letter-spacing: 1px;
            }
            QLabel#sous_titre {
                font-size: 13px;
                color: #a4b0be;
                line-height: 1.4;
                margin-bottom: 5px;
            }
            QFrame#carte_form {
                background-color: #1b1e2b;
                border-radius: 12px;
                border: 1px solid #2f3542;
            }
            QLabel#label_form {
                font-size: 13px;
                font-weight: bold;
                color: #dfe4ea;
            }
            QLabel#label_erreur {
                color: #ff4757;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #262b3d;
                border: 1px solid #3d445b;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #f1f2f6;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #ff4757;
                background-color: #2c3247;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #262b3d;
                color: #f1f2f6;
                selection-background-color: #ff4757;
                selection-color: white;
                border: 1px solid #3d445b;
            }
            QPushButton#bouton_principal {
                background-color: #ff4757;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 12px 20px;
                border: none;
            }
            QPushButton#bouton_principal:hover {
                background-color: #ff6b81;
            }
            QPushButton#bouton_principal:pressed {
                background-color: #eb2f06;
            }
            QPushButton#bouton_secondaire {
                background-color: #2f3542;
                color: #f1f2f6;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 12px 20px;
                border: 1px solid #57606f;
            }
            QPushButton#bouton_secondaire:hover {
                background-color: #3d445b;
            }
            QPushButton#bouton_secondaire:pressed {
                background-color: #1e272c;
            }
        """
        self.setStyleSheet(style_feuille)

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
    
    def get_layout_principal(self) -> QVBoxLayout:
        '''
        Retourne: Layout Principal de la fenêtre
        '''
        return self.__layout_principal

    def on_text_changed(self, texte):
        '''
        Effectuee a chaque changement de l'input.

        Entrée: Texte dans la boîte de texte.
        '''
        pass

    def verification_reponse_budget(self, reponse_budget: int) -> int:
        '''
        Verifie que la valeur entree par l'utilisateur comme budget est valide (non-nulle et entre X1 et X2)
        '''
        valeur_min = 0
        valeur_max = 0
        if reponse_budget > valeur_max or reponse_budget < valeur_min:
            raise ErreurInputBudgetFilm(f"Valeur minimale possible: {valeur_max} | Valeur maximale possible: {valeur_min} | Valeur entree: {reponse_budget}")
        
        return reponse_budget
        
    def predire(self) -> bool:
        '''
        Prédire est la fonction actionnée quand le bouton 'prédire' est pressé. 

        Entrée: self (fenêtre principale)
        Retourne: True / False
        '''

        # Vérification valeur genre
        valeur_reponse_genre = self.question_genre.currentText()
        if valeur_reponse_genre == "Sélectionnez un genre" or valeur_reponse_genre == "Genre":
            dialog = Dialogue("Veuillez entrer un genre valide.", "OK")
            dialog.activation()
        else: 
            reponse_genre_valide = True

        # Vérification valeur Rating
        valeur_reponse_score = self.question_rating.text()
        try: 
            valeur_reponse_score = float(valeur_reponse_score)
            if valeur_reponse_score < 0 or valeur_reponse_score > 10:
                dialog = Dialogue("Veuillez entrer un score sous forme de nombre à virgule entre 0 et 10.", "OK")
                dialog.activation()
            else: 
                reponse_score_valide = True
        except:
            dialog = Dialogue("Veuillez entrer un score sous forme de nombre à virgule entre 0 et 10.", "OK")
            dialog.activation()

        # Vérification réponse budget
        try:
            valeur_reponse_budget = self.verification_reponse_budget(int(self.question_budget.text()))
            reponse_budget_valide = True
        except ValueError:
            dialog = Dialogue("Veuillez entrer une réponse numérique valide pour le budget.", "OK")
            dialog.activation()

        # Vérification réponse runtime
        valeur_reponse_runtime = self.question_rating.text()
        try: 
            valeur_reponse_runtime = float(valeur_reponse_runtime)
            if valeur_reponse_runtime < 0 or valeur_reponse_runtime > 0:
                dialog = Dialogue("Veuillez entrer un runtime sous forme de nombre à virgule entre X et XXXX.", "OK")
                dialog.activation()
            else: 
                reponse_runtime_valide = True
        except:
            dialog = Dialogue("Veuillez entrer un runtime sous forme de nombre à virgule entre X et XXXX.", "OK")
            dialog.activation()

        #if reponse_score_valide and reponse_runtime_valide and reponse_genre_valide and reponse_budget_valide:
            #print("Réponse question Genre: " + valeur_reponse_genre + "\nRéponse question Budget: " + str(valeur_reponse_budget))



        # 4. Créer le tableau du film

        film = pd.DataFrame([{
            "genre": valeur_reponse_genre,
            "budget_usd": valeur_reponse_budget,
            "rating": valeur_reponse_score,
            "runtime_min": valeur_reponse_runtime
        }])
        
        # 5. Faire la prédiction
        resultat = self.modele.predire(film)
        print ("prediction du modoele :", resultat)
        
        # 6. Afficher le résultat
        if resultat == 1:
            message = "Le film est prédit comme blockbuster !"
        else:
            message = "Le film est prédit comme non-blockbuster."
        
        Dialogue(message, "OK", "Résultat de la prédiction").activation()
        
        '''
            # 1. Vérifier le genre
        genre = self.question_genre.currentText()

        if genre == "Selectionnez un genre":
            Dialogue("Veuillez sélectionner un genre.", "OK").activation()
            return

        # 2. Convertir les entrées numériques
        try:
            budget = float(self.question_budget.text())
            rating = float(self.question_rating.text())
            runtime = int(self.question_runtime.text())

        except ValueError:
            Dialogue(
                "Veuillez entrer des nombres valides.",
                "OK"
            ).activation()
            return

        # 3. Vérifier les limites
        try:
            budget = self.verification_reponse_budget(budget)

            if not 0 <= rating <= 10:
                raise ValueError("La note doit être entre 0 et 10.")

            if runtime <= 0:
                raise ErreurInputLongueurFilm(
                    "La durée doit être supérieure à 0."
                )

        except (ValueError, ErreurInputBudgetFilm,
                ErreurInputLongueurFilm) as erreur:

            Dialogue(str(erreur), "OK").activation()
            return

        '''

    def generer_graphique(self):
        '''
        Générer Graphique est la fonction actionnée quand le bouton "Générer Graphique" est pressé.
        '''
        pass


class Dialogue(QDialog):
    """
    Objet héritant de QDialog créant une fenêtre de dialogue avec une ligne de texte et un bouton permettant de sortir.
    """
    def __init__(self, texte: str, texte_bouton: str):
        super().__init__()
        self.setWindowTitle("Prediction")
        self.setMinimumWidth(320)
        
        layout_dialog = QVBoxLayout(self)
        layout_dialog.setContentsMargins(25, 25, 25, 25)
        layout_dialog.setSpacing(15)
        
        label = QLabel(texte, self)
        label.setWordWrap(True)
        label.setStyleSheet("color: #1b1e2b; font-size: 13px;")
        layout_dialog.addWidget(label)
        
        bouton = QPushButton(texte_bouton, self)
        bouton.setStyleSheet("""
            QPushButton {
                background-color: #ff4757;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #ff6b81;
            }
        """)
        layout_dialog.addWidget(bouton)
        bouton.clicked.connect(self.accepter_dialogue)

    def accepter_dialogue(self):
        self.accept()

    def activation(self):
        self.exec()