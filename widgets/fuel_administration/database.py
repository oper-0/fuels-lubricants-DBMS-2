import sqlite3
from PyQt6.QtGui import QStandardItem, QStandardItemModel

from widgets.fuel_administration.marking_logic import MarkableItem
from widgets.fuel_administration.model_utils import create_model


# Функция для установки соединения с базой данных
def setup_database(db_path):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        return connection, cursor
    except sqlite3.Error as e:
        print("Ошибка при подключении к базе данных:", e)
        return None, None


# Класс для управления базой данных
class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    # Метод для подключения к базе данных
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Ошибка при подключении к базе данных:", e)

    # Метод для отключения от базы данных
    def disconnect(self):
        if self.connection:
            self.connection.close()

    # Метод для выполнения SQL-запроса "/home/roman/SQLiteStudio/Naznachenie_db"
    def execute_query(self, query):
        try:
            return self.cursor.execute(query).fetchall()
        except sqlite3.Error as e:
            print("Ошибка при выполнении SQL-запроса:", e)
            return []

    # Метод для загрузки данных в модель
    def load_data_to_model(self, headers):
        model = create_model(headers)
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
            for row_data in result:
                row_items = []
                for column_index, item_data in enumerate(row_data):
                    if headers[column_index] == "Обозначение ХК":
                        item = MarkableItem(str(item_data))
                    else:
                        item = QStandardItem(str(item_data))
                    row_items.append(item)
                model.appendRow(row_items)
            return model
        except sqlite3.Error as e:
            print("Ошибка при выполнении SQL-запроса:", e)
            return None

    # Метод для добавления новых данных в модель
    def add_data_to_model(self, headers, new_data):
        model = create_model(headers)
        try:
            row_items = [MarkableItem(str(new_data[item])) for item in headers]
            model.appendRow(row_items)
            return model
        except Exception as e:
            print("Ошибка при добавлении данных в модель:", e)
            return None
