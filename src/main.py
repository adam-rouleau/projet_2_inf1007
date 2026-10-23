import sys

from PyQt6.QtWidgets import (
    QApplication,
)

from interface import FenetrePrincipale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = FenetrePrincipale()
    main_window.show()
    app.exec()