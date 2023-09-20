from PyQt6.QtWidgets import QWidget, QTabWidget, QTableWidget, QVBoxLayout, QLabel, QTableWidgetItem


class MainTableWidget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        tab1 = QTableWidget(0,0)
        # tab1.setItem(0, 0, QTableWidgetItem("test caption 1"))
        # tab2 = QTableWidget(30,30)
        # tab2.setItem(0, 0, QTableWidgetItem("test caption 2"))
        # tab3 = QTableWidget(30,30)
        # tab3.setItem(0, 0, QTableWidgetItem("test caption 3"))

        self.tabs.addTab(tab1, 'tab 1')
        # self.tabs.addTab(tab2, 'tab 2')
        # self.tabs.addTab(tab3, 'tab 3')

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def add_tab(self, widget: QWidget, name: str):
        idx = self.tabs.addTab(widget, name)
        self.tabs.setCurrentIndex(idx)

    def delete_tab(self):...

