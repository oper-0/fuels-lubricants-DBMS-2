from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, \
    QTreeWidget, QTreeWidgetItem

from infrastructure.types import ObjectBrowserAssets
from widgets.search_box import SearchBoxWidget
from widgets.spacers import HSpacer


class DBTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        # self.table_ico = table_ico
        self.categories: list[QTreeWidgetItem] = []

        self.setUpUI()

    def setUpUI(self):
        self.setColumnCount(1)

    def addCategory(self, category_ico: QIcon, category_name):
        # category = QTreeWidgetItem(category_name)
        category = QTreeWidgetItem()
        category.setText(0, category_name)
        category.setIcon(0, category_ico)
        self.addTopLevelItem(category)
        self.categories.append(category)

    def addTable(self, table_ico: QIcon, table_name):
        tbl = QTreeWidgetItem()
        tbl.setText(0, table_name)
        tbl.setIcon(0, table_ico)
        self.addTopLevelItem(tbl)

    def addToCategory(self, categoryName: str, item_ico: QIcon, item_name):
        category_names = [c.text(0) for c in self.categories]
        category_idx = -1
        try:
            category_idx = category_names.index(categoryName)
        except ValueError:
            raise ValueError(
                "В дереве объектов нет категории {}\nСуществующие категории:{}".format(categoryName, category_names))

        if category_idx == -1:
            raise ValueError("Magic code is not working here. Seek for bugs above me ᓚᘏᗢ")

        tmp_child = QTreeWidgetItem()
        tmp_child.setText(0, item_name)
        tmp_child.setIcon(0, item_ico)
        self.categories[category_idx].addChild(tmp_child)

    # def addItem_table(self, label):
    #     itm = DBListWidgetItem(self.table_ico, label)
    #     self.addItem(itm)


class CustomComboBox(QWidget):

    def __init__(self, cbox_ico: QIcon):
        super().__init__()

        self.cbox_ico = cbox_ico

        layout = QVBoxLayout()

        self.pm_label = QLabel()
        self.pm_label.setPixmap(cbox_ico.pixmap(QSize(24, 24)))

        # self.setMinimumSize(48, 48)

        # self.setContentsMargins(0, 0, 0, 0, )
        # layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)
        self.pm_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.pm_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        # self.setStyleSheet('border: 1px solid black;')

        layout.addWidget(self.pm_label)

        self.setLayout(layout)


class DBFilesBrowser(QWidget):

    # def __init__(self,
    #              search_ico: QIcon,
    #              arrow_ico: QIcon,
    #              table_ico: QIcon):
    def __init__(self, assets: ObjectBrowserAssets, ):
        """
        @param assets: structure for icons keep
        @param BDTableStructure: structure of db table structure. see get_db_structure() in db_interface ABC
        """
        super().__init__()

        self.assets = assets
        self.dbStruct = None

        self.setup_ui()

    def update_data(self, DBTableStructure: dict) -> None:
        self.dbStruct = DBTableStructure
        self.fillUp()

    def fillUp(self):
        for cat in self.dbStruct:
            if not isinstance(self.dbStruct[cat], list):
                # single table
                self.item_list.addTable(self.assets.norms_ico, cat)
            else:
                # table group
                self.item_list.addCategory(self.assets.folder_ico, cat)
                for tbl in self.dbStruct[cat]:
                    self.item_list.addToCategory(self.dbStruct[cat], self.assets.norms_ico, tbl)

    def setup_ui(self):
        self.top_label = QLabel("Все объекты базы")
        self.top_label.setFont(QFont('Courier New', 14))
        self.top_label.setStyleSheet("color : gray; }")
        spacer = HSpacer()
        self.obj_type_cBox = CustomComboBox(self.assets.arrow_ico)

        self.search_box = SearchBoxWidget(self.assets.search_ico)

        self.item_list = DBTreeWidget()

        self.item_list.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.top_label)
        header_layout.addWidget(spacer)
        header_layout.addWidget(self.obj_type_cBox)
        # header_layout.

        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.search_box)
        main_layout.addWidget(self.item_list)

        self.setLayout(main_layout)