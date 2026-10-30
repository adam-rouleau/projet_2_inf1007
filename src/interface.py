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
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        self.__layout_principal = QVBoxLayout()
        widget_principal.setLayout(self.__layout_principal)

        # Titre Principal
        titre_application = QLabel("Prédicteur de succès au Box Office")
        titre_application.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre_application.setObjectName("titre")
        self.__layout_principal.addWidget(titre_application)

        # Description Principale
        titre_application = QLabel("Entrez les données d'un film et découvrez s'il sera un succès ! \n Le film est considéré un succès si le revenu est 3x le budget ainsi qu'au-dessus de 100M$.")
        titre_application.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre_application.setObjectName("sous_titre")
        self.__layout_principal.addWidget(titre_application)

        # Forms 
        layout_questions = QVBoxLayout()
        self.__layout_principal.addLayout(layout_questions)

        label_question_comedie = QLabel("Genre")
        self.__layout_principal.addWidget(label_question_comedie)
        self.question_genre = QComboBox()
        self.question_genre.addItems(["Comédie", 
                                      "Science-Fiction", 
                                      "Horreur", 
                                      "Documentaire", 
                                      "Action", 
                                      "Suspense", 
                                      "Romance", 
                                      ])
        self.__layout_principal.addWidget(self.question_genre)

        self.question_budget = self.ajouter_form("Budget (USB) - Entre X et X2", layout_questions, "Reponse Placeholder")
        self.question_budget.textChanged.connect(self.on_text_changed)

        self.question_rating = self.ajouter_form("Rating", layout_questions, "Reponse Placeholder")
        self.question_rating.textChanged.connect(self.on_text_changed)

        self.question_runtime = self.ajouter_form("Runtime", layout_questions, "Reponse Placeholder")
        self.question_runtime.textChanged.connect(self.on_text_changed)


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
        
    def predire(self) -> bool:
        '''
        Prédire est la fonction actionnée quand le bouton 'prédire' est pressé. 

        Entrée: self (fenêtre principale)
        Retourne: True / False
        '''
        valeur_reponse_genre = self.verification_reponse_genre(self.question_genre.currentText())
        valeur_reponse_budget = self.verification_reponse_budget(int(self.question_budget.text()))
        print("Réponse question Genre: " + valeur_reponse_genre + "\nRéponse question Budget: " + valeur_reponse_budget)

        # TODO: Ajouter le processus de prediction


    def generer_graphique(self):
        '''
        Générer Graphique est la fonction actionnée quand le bouton "Générer Graphique" est pressé.

        Entrée: self (fenêtre principale)
        Retourne:
        '''