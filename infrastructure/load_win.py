from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel


class LoadWin(QDialog):
    def __init__(self, pic_path):
        QDialog.__init__(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.resize(500, 333)

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

        title = QLabel(self)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        # title.move(200,200)
        pixmap = QPixmap(pic_path)
        title.setPixmap(pixmap)

        self.show()