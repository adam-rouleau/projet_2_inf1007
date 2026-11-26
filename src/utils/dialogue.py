from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class Dialogue(QDialog):
    """
    Fenetre de dialogue contenant un message et un bouton de fermeture.
    """
    def __init__(self, texte: str, texte_bouton: str):
        super().__init__()
        self.setObjectName("dialogue_message")
        self.setWindowTitle("Prediction")
        self.setMinimumWidth(320)

        layout_dialog = QVBoxLayout(self)
        layout_dialog.setContentsMargins(25, 25, 25, 25)
        layout_dialog.setSpacing(15)

        label = QLabel(texte, self)
        label.setWordWrap(True)
        label.setObjectName("message")
        layout_dialog.addWidget(label)

        bouton = QPushButton(texte_bouton, self)
        bouton.setObjectName("bouton_message")
        layout_dialog.addWidget(bouton)
        bouton.clicked.connect(self.accepter_dialogue)

    def accepter_dialogue(self):
        self.accept()

    def activation(self):
        self.exec()
