import sys

from PyQt6.QtWidgets import (
    QApplication,
)

from interface import FenetrePrincipale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = FenetrePrincipale()
    with open('src/style_interface.qss', "r") as f:
        style = f.read()
        main_window.setStyleSheet(style)

    main_window.show()
    app.exec()