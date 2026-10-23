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

        titre_application = QLabel("Prédicteur de succès au Box Office")
        titre_application.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre_application.setObjectName("titre")
        self.__layout_principal.addWidget(titre_application)

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

        self.question_2 = self.ajouter_form("Budget", layout_questions, "Reponse Placeholder")
        self.question_2.textChanged.connect(self.on_text_changed)

        self.question_3 = self.ajouter_form("Rating", layout_questions, "Reponse Placeholder")
        self.question_3.textChanged.connect(self.on_text_changed)

        self.question_4 = self.ajouter_form("Runtime", layout_questions, "Reponse Placeholder")
        self.question_4.textChanged.connect(self.on_text_changed)


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
        Fonction effectuée chaque fois que le texte est changé dans un form.

        Entrée: Texte dans la boîte de texte.
        '''
        pass

    def predire(self):
        '''
        Prédire est la fonction actionnée quand le bouton 'prédire' est pressé. 

        Entrée: self (fenêtre principale)
        Retourne: 
        '''
        self.valeur_question_1 = self.question_1.text()
        self.valeur_question_2 = self.question_2.text()
        print("Réponse question 1: " + self.valeur_question_1 + "\nRéponse question 2: " + self.valeur_question_2)

    def generer_graphique(self):
        '''
        Générer Graphique est la fonction actionnée quand le bouton "Générer Graphique" est pressé.

        Entrée: self (fenêtre principale)
        Retourne:
        '''