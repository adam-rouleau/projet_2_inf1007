from abc import ABC

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
    Génération de la fenêtre principale.
    '''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projet 2 - Adam Rouleau, Eliott Magnet Da Costa: Prédicteur de succès au Box Office")
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        self.__layout_principal = QVBoxLayout()
        widget_principal.setLayout(self.__layout_principal)

        # Titre Principal
        TitrePrincipal("Prédicteur du succès au box-office", self.__layout_principal)

        # Description Principale
        SousTitre("Entrez les données d'un film et découvrez s'il sera un succès ! \n Le film est considéré un succès si le revenu est 3x le budget ainsi qu'au-dessus de 100M$.", self.__layout_principal)

        # Forms 
        layout_questions = QVBoxLayout()
        self.__layout_principal.addLayout(layout_questions)

        label_question_comedie = QLabel("Genre")
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

        self.question_budget = self.ajouter_form("Budget (USB) - Entre X et X2", layout_questions, "Reponse Placeholder")
        self.question_budget.textChanged.connect(self.on_text_changed)

        self.question_rating = self.ajouter_form("Rating", layout_questions, "Reponse Placeholder")
        self.question_rating.textChanged.connect(self.on_text_changed)

        self.question_runtime = self.ajouter_form("Runtime", layout_questions, "Reponse Placeholder")
        self.question_runtime.textChanged.connect(self.on_text_changed)

        self.probleme_question = QLabel("Veuillez répondre à toutes les questions")
        self.probleme_question.setVisible(False)

        # Layout Boutons
        layout_boutons = QHBoxLayout()
        self.__layout_principal.addLayout(layout_boutons)

        self.bouton_predire = QPushButton("Prédire")
        self.bouton_predire.clicked.connect(self.predire)
        layout_boutons.addWidget(self.bouton_predire)

        self.bouton_generer_graphique = QPushButton("Générer Graphique")
        self.bouton_generer_graphique.clicked.connect(self.generer_graphique)
        layout_boutons.addWidget(self.bouton_generer_graphique)

    def ajouter_form(self, question:str, layout:QVBoxLayout, placeholder:str="") -> QLineEdit:
        '''
        La fonction ajouter_form prend une question et ajoute automatiquement un form adapté.

        Entrée: question posée, layout dans lequel le form est inséré
        Retourne: l'objet QLineEdit créé
        '''
        label_question = QLabel(question)
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

    def verification_reponse_budget(self, reponse_budget:int) -> int:
        '''
        Verifie que la valeur entree par l'utilisateur comme budget est valide (non-nulle et entre X1 et X2)
        '''
        # TODO: Ajouter les valeurs max et min (en fonction de ces memes valeurs dans la base de donnees)
        valeur_min = 0
        valeur_max = 0
        if reponse_budget > valeur_max or reponse_budget < valeur_min:
            raise ErreurInputBudgetFilm(f"Valeur minimale possible: {valeur_max} | Valeur maximale possible: {valeur_min} | Valeur entree: {reponse_budget}")
        else: 
            return reponse_budget
        
    def predire(self) -> bool | None:
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
            # TODO: Remplacer les valeurs de runtime pour le maximum et le minimum qu'on a dans la base de données
            if valeur_reponse_runtime < 0 or valeur_reponse_runtime > 0:
                dialog = Dialogue("Veuillez entrer un runtime sous forme de nombre à virgule entre X et XXXX.", "OK")
                dialog.activation()
            else: 
                reponse_runtime_valide = True
        except:
            dialog = Dialogue("Veuillez entrer un runtime sous forme de nombre à virgule entre X et XXXX.", "OK")
            dialog.activation()

        # TODO: Ajouter le processus de prediction
        if reponse_score_valide and reponse_runtime_valide and reponse_genre_valide and reponse_budget_valide:
            print("Réponse question Genre: " + str(valeur_reponse_genre) + "\nRéponse question Budget: " + str(valeur_reponse_budget))


    def generer_graphique(self):
        '''
        Générer Graphique est la fonction actionnée quand le bouton "Générer Graphique" est pressé.

        Entrée: self (fenêtre principale)
        Retourne:
        '''


class Dialogue(QDialog):
    """
    Objet héritant de QDialog créant une fenêtre de dialogue avec une ligne de texte et un bouton permettant de sortir.
    """
    def __init__(self, texte:str, texte_bouton:str):
        super().__init__()
        self.setWindowTitle("Attention")
        layout_dialog = QVBoxLayout(self)
        label = QLabel(texte, self)
        layout_dialog.addWidget(label)
        self.setMinimumSize(label.sizeHint())
        bouton = QPushButton(texte_bouton, self)
        layout_dialog.addWidget(bouton)
        bouton.clicked.connect(self.accepter_dialogue)

    def accepter_dialogue(self):
        self.accept()

    def activation(self):
        self.exec()


class TitrePrincipal(QLabel):
    """
    Ajout d'un titre principal dans le layout spécifié.
    """
    def __init__(self, contenu:str, layout:QVBoxLayout):
       super().__init__(contenu) 
       self.setAlignment(Qt.AlignmentFlag.AlignCenter)
       self.setObjectName("titre")
       layout.addWidget(self)

class SousTitre(QLabel):
    def __init__(self, contenu:str, layout:QVBoxLayout):
        super().__init__(contenu)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("sous_titre")
        layout.addWidget(self)