from PyQt6.QtCore import QPoint, QStringListModel, Qt, pyqtSignal
from PyQt6.QtWidgets import QCompleter, QHeaderView


class SearchableHeaderView(QHeaderView):
    # Сигнал об изменении текста поиска
    searchTextChanged = pyqtSignal()

    def __init__(self, orientation, headers, parent=None):
        super().__init__(orientation, parent)
        self.search_inputs = {}  # Словарь для хранения полей ввода поиска для каждого столбца
        self.headers = headers  # Заголовки столбцов
        self.parent_widget = parent  # Ссылка на родительский виджет

        # Запрос для получения уникальных значений из базы данных
        self.options_query = '''
            SELECT DISTINCT
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

        # Отображение заголовков столбцов на соответствующие столбцы в базе данных
        self.column_mapping = {
            "Изделие": "Name",
            "Силовая установка (двигатель)": "Engine",
            "Составные части комплексного изделия": "CompositeParts",
            "Марка ГСМ": "FuelBrand",
            "Марка Основная": "MainBrand",
            "Марка Дублирующая": "DuplicateBrand",
            "Марка Резервная": "ReserveBrand",
            "Обозначение ХК": "DesignationHK",
            "Дата согласования ХК": "ApprovalDateHK",
            "Срок согласования ХК": "ApprovalPeriodHK",
            "Предприятие-изготовитель изделия": "ManufacturerAbbreviation",
        }

    def mousePressEvent(self, event):
        # Обработчик события нажатия мыши
        index = self.logicalIndexAt(event.pos())
        if index >= 0:
            self.toggle_search_input(index)

    def toggle_search_input(self, column):
        # Переключение видимости поля ввода поиска для указанного столбца
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
                input_widget.setGeometry(header_pos.x(), self.parent().y() - self.height() + 40,
                                         self.sectionSize(column),
                                         self.height())
                # Always show the input widget when toggling
                input_widget.setHidden(False)
                input_widget.setFocus()

                # Получение соответствующего столбца в базе данных с использованием отображения
                db_column = self.column_mapping.get(self.headers[column], "")
                if db_column:
                    options_query = f'''
                        SELECT DISTINCT {db_column} FROM TestBd;
                    '''
                    options_result = self.parent_widget.cursor.execute(options_query).fetchall()
                    options = [str(item[0]) for item in options_result]

                    # Создание модели для QCompleter
                    model = QStringListModel(options, input_widget)

                    completer = QCompleter(model, input_widget)
                    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                    completer.setModelSorting(QCompleter.ModelSorting.CaseSensitivelySortedModel)
                    completer.setFilterMode(Qt.MatchFlag.MatchContains)

                    input_widget.setCompleter(completer)

    def filter_data(self):
        # сигнал об изменении текста поиска
        self.searchTextChanged.emit()
