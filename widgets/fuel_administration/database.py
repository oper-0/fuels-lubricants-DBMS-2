import sqlite3
from PyQt6.QtGui import QStandardItem
from widgets.fuel_administration.window import create_model


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

    # Метод для выполнения SQL-запроса
    def execute_query(self, query):
        try:
            return self.cursor.execute(query).fetchall()
        except sqlite3.Error as e:
            print("Ошибка при выполнении SQL-запроса:", e)
            return []

    # Метод для загрузки данных в модель
    def load_data_to_model(self, headers):
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
            model = create_model(headers)
            for row_data in result:
                row_items = [QStandardItem(str(item)) for item in row_data]
                model.appendRow(row_items)
            return model
        except sqlite3.Error as e:
            print("Ошибка при выполнении SQL-запроса:", e)
            return None
