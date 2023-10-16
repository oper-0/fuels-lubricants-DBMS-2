import os
import random
import sys
from datetime import datetime
from typing import Callable

import PyQt6
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView, QTableWidgetItem, QTableWidget, QHBoxLayout, \
    QWidget, QApplication

# from models.in_memory_db_helpers import NORM_FIELD_DICTIONARY


class ListTreeWidget_1_Item(QTreeWidgetItem):

    def __init__(self, obj, *__args, data, table_icon, get_alias_by_key: Callable[[str], str]):
        super().__init__(obj, *__args)
        self.data = data
        self.icon = table_icon
        self.get_alias = get_alias_by_key

        self.color_expired = QColor(255, 153, 153)
        # self.color_expiring = QColor(255, 255, 153)
        self.color_last = QColor(153, 255, 153)
        self.color_expiring = self.color_last
        column_counter = 0
        for k, v in self.data.items():
            if isinstance(v, dict):
                # self.setBackground(column_counter, self.date_color_validate(v['expiring_date']))
                self.setBackground(column_counter, self.date_color_validate(v[self.get_alias('expiring_date')]))
                if v[self.get_alias('norm_name')][-3:] in ['[П]', '[В]']:
                    column_counter += 1
                    continue
                if self.background(column_counter) != self.color_expired:
                    v[self.get_alias('norm_name')] = v[self.get_alias('norm_name')] + ' ' + random.choice(['[П]', '[В]'])
                    self.setText(column_counter, v[self.get_alias('norm_name')])
                else:
                    v[self.get_alias('norm_name')] = v[self.get_alias('norm_name')] + ' ' + '[В]'
                    self.setText(column_counter, v[self.get_alias('norm_name')])
                # self.setForeground(column_counter, QBrush(QColor(0, 0, 0)))
            column_counter += 1

    def date_color_validate(self, date: str) -> QColor:
        if datetime.strptime(date, '%Y-%m-%d').year > datetime.today().year:
            return self.color_last  # срок выйдет ток в след году (только не используйте 31 декабря)
        elif datetime.strptime(date, '%Y-%m-%d').year == datetime.today().year and datetime.strptime(
                date, '%Y-%m-%d') > datetime.today():
            return self.color_expiring  # срок истекает в этом году
        else:
            return self.color_expired  # срокистек уже

    def show_table(self, column):

        values = list(self.data.values())
        if not isinstance(values[column], dict):
            return
        data = self.data
        keys = list(data.keys())
        values = list(data.values())

        self.dialog = QWidget()
        self.dialog.setWindowTitle(values[column][self.get_alias('norm_name')])
        self.dialog.setWindowIcon(self.icon)
        # self.dialog
        layout = QHBoxLayout()
        self.dialog.setLayout(layout)

        self.table = QTableWidget()
        # self.table.setColumnCount(len(values))
        # self.table.setRowCount(1)
        self.table.setColumnCount(1)
        self.table.setRowCount(len(data[keys[column]].values()))  # i know, i know ( ´･･)ﾉ(._.`)
        # self.table.setVerticalHeaderLabels(list(self.NORM_FIELD_DICTIONARY.keys()))
        self.table.setVerticalHeaderLabels(list(self.data[self.get_alias('unit_fuel_consumption')]))
        col_count = 0
        for key, val in data[keys[column]].items():
            cur_var = ''
            if isinstance(val, str):
                cur_var = val
            if isinstance(val, int):
                cur_var = str(val)
            if isinstance(val, float):
                cur_var = str(round(val, 2))

            table_item = QTableWidgetItem(cur_var)

            if key in ['expiring_date', self.get_alias('expiring_date')]:
                table_item.setBackground(self.date_color_validate(val))
                # table_item.setForeground(QBrush(QColor(0, 0, 0)))

            self.table.setItem(col_count, 0, table_item)

            col_count += 1
        header = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().hide()
        layout.addWidget(self.table)
        self.dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.dialog.resize(400, 600)
        self.dialog.show()


class ListTreeWidget_1(QTreeWidget):

    def __init__(self, icon_dir, get_alias_by_key: Callable[[str], str]):
        super().__init__()

        self.icon_dir = icon_dir
        self.items: list[QTreeWidgetItem] = []
        self.table_icon = QIcon(os.path.join(self.icon_dir, r'stats32.png'))
        self.get_alias_by_key = get_alias_by_key

        self.itemClicked.connect(self.onItemClicked)

    def clear_items(self):
        self.items = []

    def place(self, data: list[dict], translate_dict):  # translate_dict - {key: header}
        self.clear()
        self.clear_items()

        # headers = []
        # for item in data:
        #     headers = headers+list(item)
        # headers = set(headers)
        if data[0]:
            headers = list(data[0].keys())
        else:
            headers = []

        self.setColumnCount(len(headers))
        # self.setHeaderLabels(list(translate_dict.values()))
        self.setHeaderLabels(headers)
        for item in data:
            str_arr_to_place = []
            idx_for_tables = []
            counter = -1
            for el in item.values():
                counter += 1
                if isinstance(el, int):
                    str_arr_to_place.append(str(el))
                    continue
                if isinstance(el, dict):
                    str_arr_to_place.append(el[self.get_alias_by_key('norm_name')])
                    idx_for_tables.append(counter)
                    continue
                str_arr_to_place.append(el)
            self.items.append(ListTreeWidget_1_Item(self, str_arr_to_place, data=item, table_icon=self.table_icon, get_alias_by_key=self.get_alias_by_key))
            # self.items.append(SearchResultsTreeItem(self, {'value_list': str_arr_to_place, 'data': item, 'icon_for_tables': self.table_icon}))
            for i in idx_for_tables:
                self.items[-1].setIcon(i, self.table_icon)
            # self.items[-1].setFlags(self.items[-1].flags() | Qt.ItemFlag.ItemIsUserTristate | Qt.ItemFlag.ItemIsUserCheckable)
            self.items[-1].setFlags(self.items[-1].flags() | Qt.ItemFlag.ItemIsUserCheckable)
            self.items[-1].setCheckState(0, Qt.CheckState.Unchecked)

    @PyQt6.QtCore.pyqtSlot(QTreeWidgetItem, int)
    def onItemClicked(self, it: ListTreeWidget_1_Item, col):
        print(it, col, it.text(col))
        it.show_table(col)

    def get_table(self): ...

    def get_checked_data(self):
        rezult = []
        # print('items ({}): {}'.format(len(self.items), self.items))
        for i in range(len(self.items)):
            if self.items[i].checkState(0)==Qt.CheckState.Checked:
                rezult.append(self.items[i])
        # print('checked items({}): {}'.format(len(rezult), rezult))
        return rezult

    def uncheck_all(self):
        for i in self.items:
            if i.checkState(0)==Qt.CheckState.Checked:
                i.setCheckState(0, Qt.CheckState.Unchecked)
