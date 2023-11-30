import sqlite3
from PyQt6.QtCore import Qt, QEvent, pyqtSignal, QPoint
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QFrame, QTableView, QLineEdit, QHeaderView


class SearchableHeaderView(QHeaderView):
    searchTextChanged = pyqtSignal()

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.search_inputs = {}

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index >= 0:
            self.toggle_search_input(index)

    def toggle_search_input(self, column):
        for col, input_widget in self.search_inputs.items():
            if input_widget.text():
                input_widget.setHidden(False)
            else:
                input_widget.setHidden(True)
        input_widget = self.search_inputs.get(column)
        if input_widget:
            if not input_widget.isHidden():
                input_widget.clear()
                input_widget.setHidden(True)
            else:
                header_pos = self.mapToGlobal(QPoint(self.sectionViewportPosition(column), 0))
                input_widget.setGeometry(header_pos.x(), self.parent().y() - self.height()+40, self.sectionSize(column),
                                         self.height())
                # Always show the input widget when toggling
                input_widget.setHidden(False)
                input_widget.setFocus()

    def filter_data(self):
        self.searchTextChanged.emit()


class FuelAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_database()

    def init_ui(self):
        layout = QVBoxLayout(self)

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        window_width = int(screen_rect.width() * 0.9)
        window_height = int(screen_rect.height() * 0.9)
        self.resize(window_width, window_height)
        self.move((screen_rect.width() - window_width) // 2, (screen_rect.height() - window_height) // 2)

        self.setWindowTitle('НАЗНАЧЕНИЕ')
        layout.setSpacing(0)  # Set spacing to 0
        self.count_label = QLabel('', self)
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.count_label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.count_label.setFixedWidth(int(window_width * 0.9))
        font = QFont()
        font.setPointSize(16)
        self.count_label.setFont(font)
        layout.addWidget(self.count_label)

        self.label2 = QLabel('ВВЕДИТЕ ДАННЫЕ ДЛЯ ПОИСКА', self)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.label2.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.label2.setFixedWidth(int(window_width * 0.9))
        layout.addWidget(self.label2, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.table = QTableView(self)
        self.table.setFixedWidth(int(window_width * 0.9))

        self.headers = ["Изделие", "Силовая установка (двигатель)", "Составные части комплексного изделия",
                        "Марка ГСМ", "Марка Основная", "Марка Дублирующая", "Марка Резервная", "Обозначение ХК",
                        "Дата согласования ХК", "Срок согласования ХК",
                        "Предприятие-изготовитель изделия"]

        model = self.create_model(self.headers)
        self.table.setModel(model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        header = SearchableHeaderView(Qt.Orientation.Horizontal, self)
        self.table.setHorizontalHeader(header)

        column_widths = [120, 225, 290, 140, 150, 160, 150, 150, 180, 175, 295]
        for col, width in enumerate(column_widths):
            header.resizeSection(col, width)

            search_input = QLineEdit(self)
            search_input.setPlaceholderText('Поиск...')
            search_input.setHidden(True)
            search_input.textChanged.connect(lambda text, column=col: self.update_search_criteria(text, column))
            search_input.installEventFilter(self)
            header.search_inputs[col] = search_input

        header.setFixedHeight(50)
        header.searchTextChanged.connect(self.filter_data)

        # Add a dictionary to store search criteria for each column
        self.search_criteria = {}

        # Define the vertical spacing between the header and data start
        vertical_spacing = 60

        container = QWidget(self)
        container_layout = QVBoxLayout(container)
        # Set the spacing between the header and data start
        container_layout.setSpacing(vertical_spacing)
        container_layout.addWidget(self.count_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        container_layout.addWidget(self.table, stretch=1, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(container, stretch=1, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.show()

    def create_model(self, headers):
        model = QStandardItemModel()

        for col, header in enumerate(headers):
            header_item = QStandardItem(header)
            model.setHorizontalHeaderItem(col, header_item)

        return model

    def setup_database(self):
        try:
            with sqlite3.connect("/home/roman/SQLiteStudio/Naznachenie_db") as connection:
                self.connection = connection
                self.cursor = connection.cursor()
                self.load_data_to_model()

        except sqlite3.Error as e:
            print("Ошибка при подключении к базе данных:", e)

    def load_data_to_model(self):
        select_query = '''
            SELECT
                Name, 
                Engine, 
                CompositeParts, 
                FuelBrand, 
                MainBrand, 
                DuplicateBrand, 
                ReserveBrand, 
                DesignationHK, 
                ApprovalDateHK, 
                ApprovalPeriodHK, 
                ManufacturerAbbreviation
            FROM TestBd;
        '''
        try:
            result = self.cursor.execute(select_query).fetchall()

            model = self.create_model(self.headers)
            for row_data in result:
                row_items = [QStandardItem(str(item)) for item in row_data]
                model.appendRow(row_items)

            self.table.setModel(model)

        except sqlite3.Error as e:
            print("Ошибка при выполнении SQL-запроса:", e)

    def update_search_criteria(self, text, column):
        self.search_criteria[column] = text.lower()
        self.filter_data()

    def filter_data(self):
        model = self.table.model()
        count = 0
        for row in range(model.rowCount()):
            row_visible = all(
                search_text in model.index(row, col).data().lower()
                for col, search_text in self.search_criteria.items()
            )
            self.table.setRowHidden(row, not row_visible)
            if row_visible:
                count += 1
        if count == 1:
            self.count_label.setText(f'Результаты поиска: {count} позиция')
        else:
            self.count_label.setText(f'Результаты поиска: {count} позиции')

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()


if __name__ == '__main__':
    app = QApplication([])
    window = FuelAdmin()
    app.exec()
