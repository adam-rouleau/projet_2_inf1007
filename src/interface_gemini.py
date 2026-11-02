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
)

from exceptions import (
    ErreurInputBudgetFilm, 
    ErreurInputLongueurFilm
)

class FenetrePrincipale(QMainWindow):
    '''
    FenetrePrincipale crée la fenêtre principale. 
    
    Hérite de: QMainWindow
    '''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projet 2 - Adam Rouleau, Eliott Magnet Da Costa: Prédicteur de succès au Box Office")
        self.setMinimumWidth(500)
        
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        self.__layout_principal = QVBoxLayout()
        self.__layout_principal.setContentsMargins(30, 30, 30, 30)
        self.__layout_principal.setSpacing(20)
        widget_principal.setLayout(self.__layout_principal)

        # Titre Principal
        titre_application = QLabel("Prédicteur de succès au Box Office")
        titre_application.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre_application.setObjectName("titre")
        self.__layout_principal.addWidget(titre_application)

        # Description Principale
        sous_titre_application = QLabel("Entrez les données d'un film et découvrez s'il sera un succès !\nLe film est considéré un succès si le revenu est 3x le budget ainsi qu'au-dessus de 100M$.")
        sous_titre_application.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sous_titre_application.setWordWrap(True)
        sous_titre_application.setObjectName("sous_titre")
        self.__layout_principal.addWidget(sous_titre_application)

        # Forms 
        layout_questions = QVBoxLayout()
        layout_questions.setSpacing(12)
        self.__layout_principal.addLayout(layout_questions)

        label_question_comedie = QLabel("Genre")
        label_question_comedie.setObjectName("label_form")
        layout_questions.addWidget(label_question_comedie)
        
        self.question_genre = QComboBox()
        self.question_genre.addItems(["Genre",
                                      "Comédie", 
                                      "Science-Fiction", 
                                      "Horreur", 
                                      "Documentaire", 
                                      "Action", 
                                      "Suspense", 
                                      "Romance", 
                                      ])
        layout_questions.addWidget(self.question_genre)

        self.question_budget = self.ajouter_form("Budget (USB) - Entre X et X2", layout_questions, "Ex: 50000000")
        self.question_budget.textChanged.connect(self.on_text_changed)

        self.question_rating = self.ajouter_form("Rating", layout_questions, "Ex: 7.5")
        self.question_rating.textChanged.connect(self.on_text_changed)

        self.question_runtime = self.ajouter_form("Runtime", layout_questions, "Ex: 120")
        self.question_runtime.textChanged.connect(self.on_text_changed)

        self.probleme_question = QLabel("Veuillez répondre à toutes les questions")
        self.probleme_question.setObjectName("label_erreur")
        self.probleme_question.setVisible(False)
        self.__layout_principal.addWidget(self.probleme_question)

        # Layout Boutons
        layout_boutons = QHBoxLayout()
        layout_boutons.setSpacing(15)
        self.__layout_principal.addLayout(layout_boutons)

        self.bouton_predire = QPushButton("Prédire")
        self.bouton_predire.setObjectName("bouton_principal")
        self.bouton_predire.clicked.connect(self.predire)
        layout_boutons.addWidget(self.bouton_predire)

        self.bouton_generer_graphique = QPushButton("Générer Graphique")
        self.bouton_generer_graphique.setObjectName("bouton_secondaire")
        self.bouton_generer_graphique.clicked.connect(self.generer_graphique)
        layout_boutons.addWidget(self.bouton_generer_graphique)

        # Application du style global (QSS)
        self.appliquer_styles()

    def appliquer_styles(self):
        style_feuille = """
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel#titre {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            QLabel#sous_titre {
                font-size: 13px;
                color: #7f8c8d;
                margin-bottom: 15px;
            }
            QLabel#label_form {
                font-size: 13px;
                font-weight: 600;
                color: #34495e;
            }
            QLabel#label_erreur {
                color: #e74c3c;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #dcdde1;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #2f3640;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3498db;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 0px;
            }
            QPushButton#bouton_principal {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 6px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton#bouton_principal:hover {
                background-color: #2980b9;
            }
            QPushButton#bouton_principal:pressed {
                background-color: #1f618d;
            }
            QPushButton#bouton_secondaire {
                background-color: #ecf0f1;
                color: #2c3e50;
                font-weight: bold;
                font-size: 14px;
                border-radius: 6px;
                padding: 10px 20px;
                border: 1px solid #bdc3c7;
            }
            QPushButton#bouton_secondaire:hover {
                background-color: #dde4e6;
            }
            QPushButton#bouton_secondaire:pressed {
                background-color: #bdc3c7;
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
        
    def predire(self) -> bool:
        '''
        Prédire est la fonction actionnée quand le bouton 'prédire' est pressé. 

        Entrée: self (fenêtre principale)
        Retourne: True / False
        '''

        # Vérification valeur genre
        valeur_reponse_genre = self.question_genre.currentText()
        if valeur_reponse_genre == "Genre":
            dialog = Dialogue("Veuillez entrer un genre.", "OK")
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
            dialog = Dialogue("Veuillez entrer une réponse à toutes les questions.", "OK")
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

        if reponse_score_valide and reponse_runtime_valide and reponse_genre_valide and reponse_budget_valide:
            print("Réponse question Genre: " + valeur_reponse_genre + "\nRéponse question Budget: " + str(valeur_reponse_budget))


    def generer_graphique(self):
        '''
        Générer Graphique est la fonction actionnée quand le bouton "Générer Graphique" est pressé.

        Entrée: self (fenêtre principale)
        Retourne:
        '''
        pass


class Dialogue(QDialog):
    """
    Objet héritant de QDialog créant une fenêtre de dialogue avec une ligne de texte et un bouton permettant de sortir.
    """
    def __init__(self, texte: str, texte_bouton: str):
        super().__init__()
        self.setWindowTitle("Attention")
        self.setMinimumWidth(300)
        
        layout_dialog = QVBoxLayout(self)
        layout_dialog.setContentsMargins(20, 20, 20, 20)
        layout_dialog.setSpacing(15)
        
        label = QLabel(texte, self)
        label.setWordWrap(True)
        layout_dialog.addWidget(label)
        
        bouton = QPushButton(texte_bouton, self)
        bouton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout_dialog.addWidget(bouton)
        bouton.clicked.connect(self.accepter_dialogue)

    def accepter_dialogue(self):
        self.accept()

    def activation(self):
        self.exec()