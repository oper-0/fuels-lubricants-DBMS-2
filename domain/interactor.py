from typing import Callable

from domain.db_interface import DbInterface
from domain.path_keeper import PathKeeper


class INTERACTOR(object):
    """
    Singleton класс, содержащий необходимую информацию для использования программой
    """
    paths: PathKeeper = None
    UsersLogger: Callable[[str, str], None]  # should be initialized in MainWindow
    WorkingRepository: DbInterface = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(INTERACTOR, cls).__new__(cls)
        return cls.instance