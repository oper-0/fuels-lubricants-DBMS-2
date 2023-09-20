from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QTextEdit, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QLabel


class CustomSearchButton(QWidget):

    def __init__(self, cbox_ico: QIcon):
        super().__init__()

        self.cbox_ico = cbox_ico

        layout = QVBoxLayout()

        self.pm_label = QLabel()
        self.pm_label.setPixmap(cbox_ico.pixmap(QSize(24, 24)))

        # self.setMinimumSize(48, 48)

        self.setContentsMargins(0, 0, 0, 0, )
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.pm_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        self.setStyleSheet('border: 1px solid black;')

        layout.addWidget(self.pm_label)

        self.setLayout(layout)


class SearchBoxWidget(QWidget):
    def __init__(self, btn_ico: QIcon):
        super().__init__()
        layout = QHBoxLayout()

        self.text_area = QLineEdit()
        self.text_area.setPlaceholderText('Поиск...')
        self.text_area.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        # self.text_area.placeholderText().сделать_текст_наклонным
        self.search_btn = CustomSearchButton(btn_ico)
        # self.search_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)

        layout.addWidget(self.text_area)
        layout.addWidget(self.search_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
