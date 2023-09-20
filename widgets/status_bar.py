from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QStatusBar, QHBoxLayout, QLabel


class DBStatusBarWidget(QLabel):

    def __init__(self, connected_ico_path: str, disconnected_ico_path: str):
        super().__init__()

        self.pixmap_connected = QPixmap(connected_ico_path)
        self.pixmap_disconnected = QPixmap(disconnected_ico_path)

        self.set_disconnected()

    def set_connected(self):
        self.setPixmap(self.pixmap_connected)
        self.setToolTip('База подключена')

    def set_disconnected(self):
        self.setPixmap(self.pixmap_disconnected)
        self.setToolTip('База не подключена')


class StatusBar(QStatusBar):

    def __init__(self, ico_db_connected_path: str, ico_db_disconnected_path: str):
        super().__init__()
        # layout = QHBoxLayout()
        self.db_widget = DBStatusBarWidget(ico_db_connected_path, ico_db_disconnected_path)

        self.addPermanentWidget(self.db_widget)

        self.showMessage("STATUS BAR")

    def setDBStatus_connected(self):
        self.db_widget.set_connected()

    def setDBStatus_disconnected(self):
        self.db_widget.set_disconnected()