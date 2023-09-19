import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow

from domain.interactor import INTERACTOR
from widgets.logger import LoggerWidget


class MainWindow(QMainWindow):

    def __init__(self, interactor: INTERACTOR):
        super(MainWindow, self).__init__()
        
        self.interactor = interactor

        #  widgets:
        self.TOOLBAR = None
        self.STATUS_BAR = None
        self.MENU_BAR = None
        self.LEFT_DOCK_AREA = None
        self.RIGHT_DOCK_AREA = None
        self.BOT_DOCK_AREA = None
        self.CENTRAL_TABLE_WIDGET = None
        self.LOGGER = LoggerWidget(QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'info_24.png')),
                                   QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'error_24.png')),
                                   QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'warn_24.png')),
                                   )
        self.interactor.UsersLogger = self.LOGGER.log
        self.dbTablesWidget = None

        self.setup_ui()

        self.showMaximized()

        self.LOGGER.log('База ГСМ v 0.1.1')
        self.show()
        
    def setup_ui(self):
        """
        Настраивает основное окно программы
        """
        self.setWindowTitle("БАЗА ГСМ")
        self.setWindowIcon(QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'oil-drum.png')))
        self._SetToolBar()
        self._SetMenuBar()
        self._SetLeftDockArea()
        # self._SetRightDockArea()
        self._SetCentralWidget()
        self._SetBotDockArea()
        self._SetStatusBar()

    def _SetToolBar(self):
        pass

    def _SetMenuBar(self):
        pass

    def _SetLeftDockArea(self):
        pass

    def _SetCentralWidget(self):
        pass

    def _SetBotDockArea(self):
        pass

    def _SetStatusBar(self):
        pass
        
    