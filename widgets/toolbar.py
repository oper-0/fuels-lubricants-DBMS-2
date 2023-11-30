import os
from enum import Enum

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QToolBar, QWidget, QVBoxLayout, \
    QGridLayout, QLabel


class TbG_layouts(Enum):
    grid = 1
    h_box = 2
    b_box = 3


class ToolbarGroup_Item(QWidget):

    def __init__(self, f, ico: QIcon, popup_msg: str):
        super().__init__()

        self.ico = ico
        self.setToolTip(popup_msg)
        self.f = f

        layout = QVBoxLayout()

        self.pm_label = QLabel()
        # self.pm_label.setPixmap(ico.pixmap(QSize(24,24)))
        self.pm_label.setPixmap(ico.pixmap(QSize(32, 32)))

        # self.standart_color = Qt.
        self.setAutoFillBackground(True)
        # self.setStyleSheet("Qlabel::hover"
        #                      "{"
        #                      "background-color : lightgreen;"
        #                      "}")

        # test
        # self.setMinimumSize(32,32)
        self.setMinimumSize(48, 48)
        # self.setMinimumSize(90,90)

        # self.pm_label.setStyleSheet("border: 1px solid red; background-color: lightgreen")
        self.pm_label.setStyleSheet("QLabel:hover{ 1px solid red; background-color: lightgreen}")

        self.setContentsMargins(0, 0, 0, 0, )
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.pm_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.pm_label)

        # self.eve

        self.setLayout(layout)

    def mousePressEvent(self, e):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

    def mouseReleaseEvent(self, e):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.transparent)
        self.setPalette(p)
        self.f()


class ToolbarGroup(QWidget):
    def __init__(self, title: str):
        super().__init__()

        self.title = title

        self.main_layout = QVBoxLayout()

        self.layout = QGridLayout()

        self.current_row = 0
        self.current_col = 0
        self.maxRows = 1
        self.maxCols = 4

        self.setContentsMargins(0, 0, 0, 0)

        # self.actions: list[QAction] = []

        self.main_layout.addLayout(self.layout)
        title_text = QLabel(self.title)
        title_text.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        title_text.setFont(QFont('Courier New'))
        title_text.setStyleSheet('color: gray')
        self.main_layout.addWidget(title_text)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setLayout(self.main_layout)

    def addItem(self, f, ico: QIcon, description: str):

        new_item = ToolbarGroup_Item(f, ico, description)
        self.layout.addWidget(new_item, self.current_row, self.current_col)

        self.current_col += 1

        if self.current_row > self.maxRows - 1:
            raise Exception('Group {} are overflowed. Only {} elements is permitted.'.format(self.title,
                                                                                             self.maxCols * self.maxRows))

        if self.current_col > self.maxCols - 1:
            self.current_row += 1
            self.current_col = 0


class Toolbar(QToolBar):
    def __init__(self, default_ico: QIcon):
        super().__init__()

        self.default_ico = default_ico
        print(os.getcwd())

        self.groups: list[ToolbarGroup] = []

    def add_group(self, title: str):
        group = ToolbarGroup(title)
        self.groups.append(group)
        self.addWidget(group)
        self.addSeparator()

    def add_item(self, f, group_title: str, ico: QIcon = None, description: str = 'No description provided'):
        """
        f: closure function to invoke when toolbar widget is triggered
        """
        if not ico:
            ico = self.default_ico

        group = self._get_group_by_title(group_title)
        group.addItem(f, ico, description)

    def _get_group_by_title(self, title: str):
        for g in self.groups:
            if g.title == title:
                return g
