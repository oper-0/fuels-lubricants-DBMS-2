import sys

from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QLineEdit, QApplication


class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal()  # ЛКМ на поле вводе

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)


def test_func():
    print("TEST")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    nud = ClickableLineEdit('Default text')
    nud.clicked.connect(test_func)
    nud.show()
    app.exec()
