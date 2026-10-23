from PyQt6.QtWidgets import (  
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

class FenetrePrincipale(QMainWindow):
    '''
    FenetrePrincipale crée la fenêtre principale. 
    
    Hérite de: QMainWindow
    '''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projet 2 - Adam Rouleau, Eliott Magnet Da Costa")
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)

        self.__layout_principal = QVBoxLayout()
        widget_principal.setLayout(self.__layout_principal)

        titre_application = QLabel("Titre Principal")
        titre_application.setObjectName("titre")
        self.__layout_principal.addWidget(titre_application)

        # Forms 
        layout_questions = QVBoxLayout()
        self.__layout_principal.addLayout(layout_questions)

        self.question_1 = self.ajouter_form("Question 1", layout_questions, "Reponse Placeholder")
        self.question_1.textChanged.connect(self.on_text_changed)

        self.question_2 = self.ajouter_form("Question 2", layout_questions, "Reponse Placeholder")
        self.question_2.textChanged.connect(self.on_text_changed)

        self.bouton_predire = QPushButton("Prédire")
        self.bouton_predire.clicked.connect(self.predire)
        self.__layout_principal.addWidget(self.bouton_predire)

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