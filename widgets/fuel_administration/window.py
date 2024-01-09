# Импорт необходимых модулей
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor, QFont, QImage, QPalette, QBrush
from PyQt6.QtWidgets import (
    QHeaderView, QApplication, QLabel, QVBoxLayout, QFrame, QTableView, QWidget,
    QLineEdit, QGroupBox
)
# Импорт функции show_context_menu из внешнего модуля
from widgets.fuel_administration.functions_document import show_context_menu
from widgets.fuel_administration.marking_logic import MarkableItem, mark_cell
# Импорт класса SearchableHeaderView из другого модуля
from widgets.fuel_administration.search_header_view import SearchableHeaderView


# Функция для создания QStandardItemModel на основе указанных заголовков
def create_model(headers, item_type=None):
    model = QStandardItemModel()
    headers_without_filepath = [header for header in headers if header != "FilePath"]
    for col, header in enumerate(headers_without_filepath):
        if item_type is not None:
            header_item = item_type(header)
        else:
            header_item = QStandardItem(header)
        model.setHorizontalHeaderItem(col, header_item)
    return model


class FuelAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_database()
        self.filter_data()
        self.column_mapping = {
            "ID": "Product",
            "Изделие": "Name",
            "Силовая установка (двигатель)": "Engine",
            "Составные части комплексного изделия": "CompositeParts",
            "Марка ГСМ": "FuelBrand",
            "Марка Основная": "MainBrand",
            "Марка Дублирующая": "DuplicateBrand",
            "Марка Резервная": "ReserveBrand",
            "Обозначение ХК": "DesignationHK",
            "Документ ХК": "FilePath",
            "Дата согласования ХК": "ApprovalDateHK",
            "Срок согласования ХК": "ApprovalPeriodHK",
            "Предприятие-изготовитель изделия": "ManufacturerAbbreviation",
        }

    # Инициализация пользовательского интерфейса
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setup_window_geometry()
        self.setup_main_widgets(layout)

    # Настройка основных виджетов главного окна
    def setup_main_widgets(self, layout):
        self.setWindowTitle('НАЗНАЧЕНИЕ')
        layout.setSpacing(0)
        self.setup_count_label(layout)
        self.setup_label2(layout)
        self.setup_table(layout)

    # Настройка геометрии окна приложения
    def setup_window_geometry(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        window_width = int(screen_rect.width() * 0.9)
        window_height = int(screen_rect.height() * 0.9)
        self.resize(window_width, window_height)
        self.move((screen_rect.width() - window_width) // 2, (screen_rect.height() - window_height) // 2)

    # Настройка виджета для отображения количества записей
    def setup_count_label(self, layout):
        self.count_label = QLabel('', self)
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.count_label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.count_label.setFixedWidth(int(self.width() * 0.9))
        font = QFont()
        font.setPointSize(16)
        self.count_label.setFont(font)
        layout.addWidget(self.count_label)

    # Настройка второго текстового метки
    def setup_label2(self, layout):
        self.label2 = QLabel('ВВЕДИТЕ ДАННЫЕ ДЛЯ ПОИСКА', self)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.label2.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.label2.setFixedWidth(int(self.width() * 0.9))
        layout.addWidget(self.label2, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    # Настройка таблицы данных
    def setup_table(self, layout):
        container = QGroupBox()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(60)
        self.setup_table_view(container_layout)
        layout.addWidget(container, stretch=1, alignment=Qt.AlignmentFlag.AlignHCenter)

    # Настройка представления таблицы данных
    def setup_table_view(self, layout):
        self.table = QTableView(self)
        self.table.setFixedWidth(int(self.width() * 0.9))
        self.headers = [
            "Изделие", "Силовая установка (двигатель)", "Составные части комплексного изделия",
            "Марка ГСМ", "Марка Основная", "Марка Дублирующая", "Марка Резервная", "Обозначение ХК",
            "Дата согласования ХК", "Срок согласования ХК", "Предприятие-изготовитель изделия"
        ]
        model = create_model(self.headers, MarkableItem)
        self.table.setModel(model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        header = SearchableHeaderView(Qt.Orientation.Horizontal, self.headers, self)
        self.table.setHorizontalHeader(header)

        column_widths = [120, 225, 290, 140, 150, 160, 150, 150, 180, 175, 295]
        for col, width in enumerate(column_widths):
            header.resizeSection(col, width)
            self.setup_search_input(header, col)

        header.setFixedHeight(50)
        header.searchTextChanged.connect(self.filter_data)

        self.search_criteria = {}
        self.table.clicked.connect(self.on_table_item_clicked)

        layout.addWidget(self.count_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.table, stretch=1, alignment=Qt.AlignmentFlag.AlignHCenter)

    # Настройка поля для ввода текста поиска
    def setup_search_input(self, header, col):
        search_input = QLineEdit(self)
        search_input.setPlaceholderText('Поиск...')
        search_input.setHidden(True)
        search_input.textChanged.connect(lambda text, column=col: self.update_search_criteria(text, column))
        search_input.installEventFilter(self)
        header.search_inputs[col] = search_input

    # Подключение к базе данных SQLite
    def setup_database(self):
        try:
            with sqlite3.connect("/home/roman/SQLiteStudio/Naznachenie_db") as connection:
                self.connection = connection
                self.cursor = connection.cursor()
                self.load_data_to_model()
        except sqlite3.Error as e:
            print("Ошибка при подключении к базе данных:", e)

    # Загрузка данных из базы данных в модель
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

            # Используйте QStandardItem для всех элементов
            model = create_model(self.headers)
            for row_data in result:
                row_items = [QStandardItem(str(item)) for item in row_data]
                model.appendRow(row_items)

            # Заменяем обычные элементы модели на MarkableItem только для колонки "Обозначение ХК"
            designation_hk_column_index = self.headers.index("Обозначение ХК")
            for row in range(model.rowCount()):
                item = model.item(row, designation_hk_column_index)
                if item:
                    model.setItem(row, designation_hk_column_index, MarkableItem(item.text()))

            self.table.setModel(model)
        except sqlite3.Error as e:
            print("Ошибка при выполнении SQL-запроса:", e)

            self.table.setModel(model)
        except sqlite3.Error as e:
            print("Ошибка при выполнении SQL-запроса:", e)

    # Обновление критериев поиска по тексту
    def update_search_criteria(self, text, column):
        self.search_criteria[column] = text.lower()
        self.filter_data()

    # Фильтрация данных в таблице в соответствии с заданными критериями поиска
    def filter_data(self):
        model = self.table.model()
        count = 0

        if any(self.search_criteria.values()):
            for row in range(model.rowCount()):
                row_visible = all(
                    search_text in model.index(row, col).data().lower()
                    for col, search_text in self.search_criteria.items()
                )
                self.table.setRowHidden(row, not row_visible)
                if row_visible:
                    count += 1
        else:
            count = model.rowCount()
            for row in range(model.rowCount()):
                self.table.setRowHidden(row, False)
        if count == 0:
            self.count_label.setText('Ничего не найдено')
        elif count == 1:
            self.count_label.setText(f'Результаты поиска: {count} позиция')
        else:
            self.count_label.setText(f'Всего записей в базе данных: {count}')

    # Обработка щелчка по элементу таблицы
    def on_table_item_clicked(self, index):
        column_name = self.headers[index.column()]
        if column_name == "Обозначение ХК":
            item = self.table.model().itemFromIndex(index)
            if item and isinstance(item, MarkableItem):
                mark_cell(item)
        if column_name == "Обозначение ХК":
            designation_hk = self.table.model().index(index.row(), self.headers.index("Обозначение ХК")).data()
            file_path_query = f"SELECT FilePath FROM TestBd WHERE DesignationHK = '{designation_hk}';"
            try:
                result = self.cursor.execute(file_path_query).fetchone()
                if result:
                    file_path = result[0]
                    if file_path:
                        show_context_menu(self, file_path)
            except sqlite3.Error as e:
                print("Ошибка при выполнении SQL-запроса:", e)

    # Закрытие соединения с базой данных при удалении объекта
    def __del__(self):
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()


# Запуск приложения при выполнении файла
if __name__ == '__main__':
    app = QApplication([])
    window = FuelAdmin()
    app.exec()
