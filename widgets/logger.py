import random
import string
import sys
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPalette
from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QMainWindow, QApplication


class LoggerWidget(QListWidget):

    def __init__(self, info_ico: QIcon, error_ico: QIcon, warn__ico: QIcon):
        super().__init__()

        self.setFont(QFont('Courier New', 12))

        self.info_ico = info_ico# QIcon('info_24.png')
        self.error_ico = error_ico#QIcon('error_24.png')
        self.warn_ico = warn__ico#QIcon('warn_24.png')


        self.items_limit = 50 # item limitation in listWidget, on overflowing - deletes clearing_size from top
        self.clearing_size = 25 # deletes this number of lines when limit is exited

        self.item_list: list[QListWidgetItem] = []

        # self.test_run()  # comment this

    def clear_num(self, count_from_top: int):
        for i in range(count_from_top):
            self.takeItem(0)
        self.item_list = self.items_limit[0:count_from_top]

    def log(self, msg: str, mode: str = 'info'):
        """
        @param msg: текс сообщения для вывода в лог
        @param mode: 'info' | 'error' | 'warning'
        """
        ico: QIcon
        prefix: str
        match mode:
            case 'info':
                ico = self.info_ico
                prefix = '[INFO]'
            case 'error':
                ico = self.error_ico
                prefix = '[ERRO]'
            case 'warning':
                ico = self.warn_ico
                prefix = '[WARN]'
            case _:
                raise Exception("The specified mode does not match the available. Now mode={}, but only info, "
                                "warning or error are possible".format(mode))

        item = QListWidgetItem(ico, '{}\t'.format(prefix) + msg)
        # item.setBackground(Qt.GlobalColor.white)
        self.addItem(item)
        self.item_list.append(item)
        self.update()

    def update(self):
        if len(self.item_list)>self.items_limit:
            self.clear_num(self.clearing_size)
        self.scrollToBottom()

    def test_run(self):
        size = 98
        for i in range(size):
            m = random.choice(['info', 'error', 'warning'])
            match m:
                case 'info':
                    self.log('some logging message here. '+''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=15)), m)
                case 'error':
                    self.log('some logging message here. '+''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=15)), m)
                case 'warning':
                    self.log('some logging message here. '+''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=15)), m)
