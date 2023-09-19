from PyQt6.QtWidgets import QMainWindow

from domain.interactor import INTERACTOR


class MainWindow(QMainWindow):

    def __init__(self, interactor: INTERACTOR):
        super(MainWindow, self).__init__()

        self.show()