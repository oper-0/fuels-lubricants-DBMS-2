import os
import sys
import typing

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QComboBox, QLineEdit, QFormLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, \
    QHBoxLayout, QVBoxLayout, QApplication, QCompleter, QWidget

from domain.db_interface import DbInterface
from models.in_memori_db import InMemoryDB
from models.sqlite_db import SQLITE_TABLES
from widgets.line_edit import ClickableLineEdit
from widgets.list_tree_widget import ListTreeWidget_1


class DbBrowser(QDialog):

    def __init__(self, db: DbInterface,  # db access throw model
                 icons_dir: str,
                 exporter_fn: typing.Callable[[list], None],
                 ):
        super().__init__()
        self.db = db
        self.icons_dir = icons_dir
        self.exporter_fn = exporter_fn

        self.search_results = None
        self.setModal(True)
        self.setWindowIcon(QIcon(os.path.join(self.icons_dir, r'databasesearch32.png')))
        self.combos: list[QComboBox] = []
        self.edits: list[ClickableLineEdit] = []
        self.filter_form = QFormLayout()
        self.field_list = self.db.get_headers(SQLITE_TABLES.UNITS)

        self.completers: dict[str: QCompleter] = {} # field_rus: completer
        # self.word_list = []
        for fld in self.field_list:
            word_list=list(dict.fromkeys(self.db.get_all_values_for_field(fld)))
            if not word_list:
                continue
            if not isinstance(word_list[0], str):
                word_list = [str(i) for i in word_list]
            self.completers[fld]=QCompleter(word_list, self)
            self.completers[fld].setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.set_up_window()

    def set_up_window(self):

        # Строка состояния
        self.feedback_label = QLabel()

        # buttons
        self.add_field_btn = QPushButton("Добавить параметр")
        self.add_field_btn.clicked.connect(self.add_field)

        self.del_filters_btn = QPushButton("Удалить фильтр")
        self.del_filters_btn.clicked.connect(self.del_fields)

        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.search)

        self.export_btn = QPushButton("Добавить в сводную таблицу")
        self.export_btn.clicked.connect(self.export)

        # Custom spacer
        # self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.submit_h_box = QHBoxLayout()
        self.submit_h_box.addWidget(self.feedback_label, stretch=1)
        self.submit_h_box.addWidget(self.add_field_btn, stretch=2)
        self.submit_h_box.addWidget(self.del_filters_btn, stretch=2)
        self.submit_h_box.addWidget(self.search_btn, stretch=2)

        self.main_v_box = QVBoxLayout()

        self.filter_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.filter_form.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.filter_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.add_field()
        self.render_filter_form()

        self.search_results_tree = ListTreeWidget_1(self.icons_dir, self.db.get_alias)

        # Custom spacer
        # self.Hspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.browser_lo = QVBoxLayout()
        self.browser_lo.addWidget(self.search_results_tree)

        self.tmp_layer = QHBoxLayout()
        self.tmp_layer.addWidget(QLabel(""))
        self.tmp_layer.addWidget(QLabel(""))
        self.tmp_layer.addWidget(self.export_btn)
        self.browser_lo.addLayout(self.tmp_layer)

        # self.first_h_lo = QHBoxLayout()
        self.first_v_lo = QVBoxLayout()
        self.first_v_lo.addLayout(self.main_v_box)
        self.first_v_lo.addLayout(self.browser_lo)

        self.setLayout(self.first_v_lo)

    def clearText(self, text):
        """Очистка строки состояния"""
        self.feedback_label.clear()

    def search(self):
        searching_keys_and_vals = {}
        for i in range(len(self.combos)):
            field = self.combos[i].currentText()
            key = self.db.key_field_dict
            val = self.edits[i].text()
            print('field: {}; key: {}; vak: {}'.format(field, key, val))

        for i in range(len(self.combos)):
            searching_keys_and_vals[self.combos[i].currentText()] = self.edits[i].text()

        self.search_results = self.db.find(searching_keys_and_vals)
        if self.search_results == []:
            print('[INFO] empty result')
            # return
        # self.search_results_tree.place(data=self.search_results, translate_dict=dict(
        #     zip(list(self.db.dataModel.PIVOT_FIELD_DICTIONARY.values()),
        #         self.db.dataModel.PIVOT_FIELD_DICTIONARY)))
        dict_KeyHeader = translate_dict=self.db.get_dict_KeyHeader()
        self.search_results_tree.place(data=self.search_results, translate_dict=dict_KeyHeader)


    def render_filter_form(self):
        for i in range(len(self.combos)):
            self.filter_form.addRow(self.combos[i], self.edits[i])
        # self.filter_form.addRow(self.submit_h_box)
        # self.filter_form.addRow([self.feedback_label, self.add_field_btn, self.del_filters_btn])

        self.main_v_box.addLayout(self.submit_h_box)
        self.main_v_box.addLayout(self.filter_form)


    def completer_setter_fabric(self, obj_name: str):
        def edit_click_handler():
            print('widget {} under pressure!!! (⊙_⊙;)'.format(obj_name))
            ed_names = [ed_name.objectName() for ed_name in self.edits]
            fld = self.combos[ed_names.index(obj_name)].currentText()
            completer = self.completers[fld]
            edit = self.edits[ed_names.index(obj_name)]
            edit.setCompleter(completer)

        return edit_click_handler

    def add_field(self):

        self.combos.append(QComboBox(self))
        self.combos[-1].addItems(self.field_list)
        self.combos[-1].setPlaceholderText("Выберите свойство")
        self.combos[-1].setObjectName("combo_{}".format(len(self.combos)))

        # self.edits.append(QLineEdit(self))
        self.edits.append(ClickableLineEdit(self))
        self.edits[-1].setPlaceholderText("<- Выберите свойство")
        self.edits[-1].textEdited.connect(self.clearText)
        # self.edits[-1].textEdited.connect(self.contextTips)
        self.edits[-1].setObjectName("edit_{}".format(len(self.edits)))

        self.edits[-1].clicked.connect(self.completer_setter_fabric(self.edits[-1].objectName()))
        # SEARCH BY OBJECT NAME!!!!!!!!!!!!!!!!!
        # word_list = []
        # for fld in self.interactor.db.get_headers():
        #     self.word_list+=self.interactor.db.get_all_values_for_field(fld)
        # self.word_list = list(dict.fromkeys(self.word_list))
        # self.completer = QCompleter(self.word_list, self)
        # self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # self.edits[-1].setCompleter(self.completer)

        self.render_filter_form()

        # for i in self.combos:
        #     print(i.objectName())
        # for i in self.edits:
        #     print(i.objectName())

    def contextTips(self):
        pass

    def del_fields(self):
        if len(self.combos) == 1:
            return
        self.combos = self.combos[:-1]
        self.edits = self.edits[:-1]
        self.filter_form.removeRow(self.filter_form.rowCount() - 1)

    def export(self):
        # self.search_results_tree.get_table()
        # pass
        checked_search_tree_items = self.search_results_tree.get_checked_data()
        self.exporter_fn(checked_search_tree_items)  # todo self.search_results_tree.get_table() must be used and insert only checked records
        self.search_results_tree.uncheck_all()
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    nud = DbBrowser(db=InMemoryDB(r'C:\Users\4NR_Operator_34\PycharmProjects\fuels-lubricants-DBMS-2\tmp'),
                    icons_dir=r'C:\Users\4NR_Operator_34\PycharmProjects\fuels-lubricants-DBMS-2\assets\icons')
    nud.show()
    app.exec()
