import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QDockWidget, QWidget

from domain.interactor import INTERACTOR
from infrastructure.types import ObjectBrowserAssets
from widgets.db_files_browser import DBFilesBrowser
from widgets.logger import LoggerWidget
from widgets.norm_template_provider import NormTemplateProviderStartWindow
from widgets.status_bar import StatusBar
from widgets.toolbar import Toolbar


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
        """
        Настраивает ToolBar основного окна.
        Создает кнопки. Привязывает события.
        :return:
        """
        self.TOOLBAR = Toolbar(
            default_ico=QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'question-mark_24.png')))

        # База
        self.TOOLBAR.add_group("База")

        self.TOOLBAR.add_item(self._open_db,
                              "База",
                              QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'folder_32.png')),
                              'Открыть')

        self.TOOLBAR.add_item(lambda: print("[ running saving file script ]\t{ not implemented }"),
                              "База",
                              QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'diskette_32.png')),
                              'Сохранить')

        self.TOOLBAR.add_item(lambda: print("[ running change_user file script ]\t{ not implemented }"),
                              "База",
                              QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'change_32.png')),
                              'Сменить пользователя')

        self.TOOLBAR.add_item(lambda: print("[ running opening file script ]\t{ not implemented }"),
                              "База",
                              # QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'database_export_32.png')),
                              description='Открыть')

        # Модули
        self.TOOLBAR.add_group("Модули")

        self.TOOLBAR.add_item(lambda: print("[ running Назначение file script ]\t{ not implemented }"),
                              "Модули",
                              QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'target_32.png')),
                              'Назначение')

        self.TOOLBAR.add_item(lambda : print('implement me'),#self._normalization,
                              "Модули",
                              QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'fuel_32.png')),
                              'Нормирование')

        self.TOOLBAR.add_item(self._norm_template_provide,
                              # lambda: self.interactor.UsersLogger('IMPLEMENT ME!', 'error'),
                              "Модули",
                              QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'edit-tools32.png')),
                              'Создать норму')

        # Экспорт
        self.TOOLBAR.add_group("Экспорт")

        self.TOOLBAR.add_item(lambda: print("[ running Экспорт xlsx file script ]\t{ not implemented }"),
                              "Экспорт",
                              QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'xls32.png')),
                              'Экспорт XLSX')

        self.TOOLBAR.add_item(lambda: print("[ running Печать file script ]\t{ not implemented }"),
                              "Экспорт",
                              QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'printer32.png')),
                              'Печать')

        self.addToolBar(self.TOOLBAR)

    def _SetMenuBar(self):
        """
        Настраивает MenuBar.
        Создает элементы MenuBar'a. Привязывает события.
        """
        self.MENU_BAR = self.menuBar()
        self.MENU_BAR.setNativeMenuBar(False)

        file_menu = self.MENU_BAR.addMenu("Файл")
        main_menu = self.MENU_BAR.addMenu("Главная")
        make_menu = self.MENU_BAR.addMenu("Создание")
        export_menu = self.MENU_BAR.addMenu("Внешние данные")


    def _SetLeftDockArea(self):
        self.LEFT_DOCK_AREA = QDockWidget()

        assets = ObjectBrowserAssets()
        assets.search_ico = QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'search_ico_16.png'))
        assets.arrow_ico = QIcon(
            os.path.join(self.interactor.paths.abs_icons_dir, 'down-filled-triangular-arrow_16.png'))
        assets.norms_ico = QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'stats32.png'))
        assets.folder_ico = QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'folder-horizontal32.png'))

        self.dbTablesWidget = DBFilesBrowser(assets)

        if self.interactor.WorkingRepository:
            self.dbTablesWidget.update_data(self.interactor.WorkingRepository.get_db_structure())

        self.LEFT_DOCK_AREA.setWidget(self.dbTablesWidget)
        self.LEFT_DOCK_AREA.setFloating(True)
        self.LEFT_DOCK_AREA.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.LEFT_DOCK_AREA)

    def _SetCentralWidget(self):
        pass

    def _SetBotDockArea(self):
        pass

    def _SetStatusBar(self):
        self.STATUS_BAR = StatusBar(
            ico_db_connected_path=os.path.join(self.interactor.paths.abs_icons_dir, 'db_ok_24.png'),
            ico_db_disconnected_path=os.path.join(self.interactor.paths.abs_icons_dir, 'db_notok_24.png'))
        self.setStatusBar(self.STATUS_BAR)
        
    def _open_db(self):
        ...

    def _norm_template_provide(self):
        self.interactor.UsersLogger('Запуск модуля "Шаблоны норм расхода"', 'info')
        self.WINDOW_NORM_TEMPLATE_PROVIDER = NormTemplateProviderStartWindow(self.interactor.paths.abs_templates_dir,
                                                                             self.interactor.paths.abs_icons_dir)
        self.WINDOW_NORM_TEMPLATE_PROVIDER.show()