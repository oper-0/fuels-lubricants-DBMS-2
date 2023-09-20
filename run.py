import os
import sys

from PyQt6.QtWidgets import QApplication

from domain.interactor import INTERACTOR
from domain.path_keeper import PathKeeper
from infrastructure.load_win import LoadWin
from widgets.main_window import MainWindow


def load_app():
    cwd = os.getcwd()
    print('working dir is: {}'.format(cwd))

    """     setting interactor      """

    interactor = INTERACTOR()

    # paths for accessing assets
    paths = PathKeeper()
    paths.abs_root_dir = os.path.join(cwd)
    paths.abs_icons_dir = os.path.join(cwd, 'assets', 'icons')
    paths.abs_default_repositories_dir = os.path.join(cwd, 'databases')
    paths.abs_docs_export_dir = os.path.join(cwd, 'locals', 'docs')
    paths.abs_templates_dir = os.path.join(cwd, 'locals', 'templates')
    paths.abs_temporary_files_dir = os.path.join(cwd, 'tmp')
    interactor.paths = paths

    # explicit reassignment of the value for clarity, the value will be assigned after opening the db and validating it
    interactor.WorkingRepository = None

    app = QApplication(sys.argv)
    loadWindow = LoadWin(os.path.join(interactor.paths.abs_icons_dir, 'andrew-theophilopoulos-link (1).jpg'))
    app.processEvents()
    main_window = MainWindow(interactor)
    loadWindow.close()

    app.exec()



load_app()