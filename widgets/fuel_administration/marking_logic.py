from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QStandardItem


class MarkableItem(QStandardItem):
    """Класс для элемента с возможностью отметки."""

    def __init__(self, text=''):
        super().__init__(text)
        self.setCheckable(True)
        self.setCheckState(Qt.CheckState.Unchecked)


def mark_cell(item):
    """Маркировка ячейки."""
    if item and isinstance(item, MarkableItem):
        if item.checkState() == Qt.CheckState.Checked:
            item.setBackground(QColor("red"))
        else:
            item.setBackground(QColor("white"))