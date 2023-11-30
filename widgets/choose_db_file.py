import os.path
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QApplication

from domain.interactor import INTERACTOR
from models.in_memori_db import InMemoryDB
from models.sqlite_db import SqliteDatabase


class OpenDBFileWindow(QFileDialog):
    def __init__(self, interactor: INTERACTOR):
        """
        Окно поиска и выбора БД в файловой системе
        """
        super().__init__()

        self.interactor = interactor
        self.fileExtension = '.gsm'

        self.setModal(True)
        self.setWindowIcon(QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'data_base_32.png')))

        options = QFileDialog.Option.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Выберите базу данных", interactor.paths.abs_default_repositories_dir,
                                                  "gsm Files (*{})".format(self.fileExtension), options=options)
        if fileName:
            # self.interactor.UsersLogger('[IMPLEMENT ME!] Opened DB file - {}.'.format(fileName), 'info')
            self.interactor.UsersLogger(fileName, 'info')
            self.validate_db(fileName)
            return
        self.interactor.UsersLogger('Canceled opening DB file', 'info')

    def validate_db(self, filename: str):
        required_extension = self.fileExtension[1:]

        if filename[-3:] != required_extension:
            self.interactor.UsersLogger('Неподдерживаемый формат базы. Файл должен быть формата ".{}"'.format(required_extension), 'error')
            return

        self.interactor.WorkingRepository = SqliteDatabase(filename)
        # self.interactor.WorkingRepository = InMemoryDB(tmp_dir_path=self.interactor.paths.abs_temporary_files_dir)
