import os
from datetime import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDateEdit, \
    QFileDialog

from widgets.fuel_administration.database import DatabaseManager


def add_data_handler(table):
    # Создаем диалоговое окн
    dialog = QDialog()
    # Создаем QLabel для фонового изображения
    background_label = QLabel(dialog)
    background_label.setPixmap(QPixmap("assets/icons/background_navigation_add.jpg"))
    background_label.setGeometry(0, 0, 800, 600)
    dialog.setWindowTitle("Добавление новых данных")
    # Создаем виджет для кнопки загрузки файла
    file_button = QPushButton("Выбрать файл")
    file_button.setStyleSheet("""
        QPushButton {
            background-color: #f1dbf8;
            border: 3px solid #555;
            border-radius: 15px;
        }
    """)
    file_button.setFixedSize(350, 35)

    common_style = """
        QLineEdit {
            border: 2px solid #000;
        }
    """
    # Устанавливаем фоновое изображение в родительское окно
    dialog.setStyleSheet("QDialog {background-image: url(assets/icons/background_navigation_add.jpg)}")

    # Добавляем обработчик события для кнопки выбора файла
    def on_file_button_clicked():
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_path, _ = file_dialog.getOpenFileName(dialog, "Выберите файл", "", "All Files (*)")
        if file_path:
            # Устанавливаем имя файла без расширения в поле Обозначение ХК
            filename_without_extension, _ = os.path.splitext(os.path.basename(file_path))
            designation_hk_input.setText(filename_without_extension)
            dialog.file_path = file_path

    # Подключаем обработчик события к кнопке выбора файла
    file_button.clicked.connect(on_file_button_clicked)
    # Создаем виджеты для ввода данных
    name_input = QLineEdit()
    name_input.setStyleSheet(common_style)
    engine_input = QLineEdit()
    engine_input.setStyleSheet(common_style)
    composite_parts_input = QLineEdit()
    composite_parts_input.setStyleSheet(common_style)
    fuel_brand_input = QLineEdit()
    fuel_brand_input.setStyleSheet(common_style)
    main_brand_input = QLineEdit()
    main_brand_input.setStyleSheet(common_style)
    duplicate_brand_input = QLineEdit()
    duplicate_brand_input.setStyleSheet(common_style)
    reserve_brand_input = QLineEdit()
    reserve_brand_input.setStyleSheet(common_style)
    designation_hk_input = QLineEdit()
    designation_hk_input.setStyleSheet(common_style)
    approval_date_hk_input = QDateEdit()
    approval_date_hk_input.setStyleSheet(common_style)
    approval_date_hk_input.setCalendarPopup(True)
    approval_date_hk_input.setDisplayFormat("yyyy-MM-dd")
    today_date = QDate.currentDate()
    approval_date_hk_input.setDate(today_date)
    approval_period_hk_input = QLineEdit()
    approval_period_hk_input.setStyleSheet(common_style)
    manufacturer_abbreviation_input = QLineEdit()
    manufacturer_abbreviation_input.setStyleSheet(common_style)

    # Кнопки "ОК" и "Отмена"
    ok_button = QPushButton("ОК")
    ok_button.setStyleSheet("""
                QPushButton {
                    background-color: #f1dbf8;
                    border: 3px solid #555;
                    border-radius: 15px;
                }
            """)
    ok_button.setFixedSize(150, 40)

    cancel_button = QPushButton("Отмена")
    cancel_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f1dbf8;
                        border: 3px solid #555;
                        border-radius: 15px;
                    }
                """)
    cancel_button.setFixedSize(150, 40)

    # Располагаем виджеты в компоновке
    layout = QVBoxLayout(dialog)
    layout.addWidget(QLabel("Изделие:"))
    layout.addWidget(name_input)
    layout.addWidget(QLabel("Силовая установка (двигатель):"))
    layout.addWidget(engine_input)
    layout.addWidget(QLabel("Составные части комплексного изделия:"))
    layout.addWidget(composite_parts_input)
    layout.addWidget(QLabel("Марка ГСМ:"))
    layout.addWidget(fuel_brand_input)
    layout.addWidget(QLabel("Марка Основная:"))
    layout.addWidget(main_brand_input)
    layout.addWidget(QLabel("Марка Дублирующая:"))
    layout.addWidget(duplicate_brand_input)
    layout.addWidget(QLabel("Марка Резервная:"))
    layout.addWidget(reserve_brand_input)
    layout.addWidget(QLabel("Обозначение ХК:"))
    layout.addWidget(designation_hk_input)
    layout.addWidget(file_button)
    layout.addWidget(QLabel("Дата согласования ХК 'гггг-мм-дд':"))
    layout.addWidget(approval_date_hk_input)
    layout.addWidget(QLabel("Срок согласования ХК:"))
    layout.addWidget(approval_period_hk_input)
    layout.addWidget(QLabel("Предприятие-изготовитель изделия:"))
    layout.addWidget(manufacturer_abbreviation_input)

    layout.addWidget(ok_button)
    layout.addWidget(cancel_button)
    # Создаем горизонтальную компоновку только для кнопок
    button_layout = QHBoxLayout()
    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)
    # Добавляем горизонтальную компоновку кнопок в основную вертикальную компоновку
    layout.addLayout(button_layout)

    # Обработчики событий для кнопок
    def on_ok_button_clicked(headers):
        # Проверяем ввод даты
        try:
            # Предполагая, что формат даты - YYYY-MM-DD
            approval_date = QDate.fromString(approval_date_hk_input.text(), 'yyyy-MM-dd')
            datetime.strptime(approval_date.toString('yyyy-MM-dd'), '%Y-%m-%d').date()
        except ValueError:
            QMessageBox.warning(dialog, "Ошибка", "Неверный формат даты")
            return

        # Проверяем все поля на заполненность
        if not all([
            name_input.text(),
            engine_input.text(),
            composite_parts_input.text(),
            fuel_brand_input.text(),
            main_brand_input.text(),
            duplicate_brand_input.text(),
            reserve_brand_input.text(),
            designation_hk_input.text(),
            approval_date_hk_input.text(),
            approval_period_hk_input.text(),
            manufacturer_abbreviation_input.text()
        ]):
            QMessageBox.warning(dialog, "Ошибка", "Заполните все данные!")
            return
        # Если все в порядке, принимаем диалог
        dialog.accept()

    def on_cancel_button_clicked():
        dialog.reject()

    ok_button.clicked.connect(on_ok_button_clicked)
    cancel_button.clicked.connect(on_cancel_button_clicked)
    # Показываем диалоговое окно
    result = dialog.exec()
    # Если пользователь нажал "ОК", возвращаем данные, иначе возвращаем None
    if result == QDialog.DialogCode.Accepted:
        new_data = {
            "Name": name_input.text(),
            "Engine": engine_input.text(),
            "CompositeParts": composite_parts_input.text(),
            "FuelBrand": fuel_brand_input.text(),
            "MainBrand": main_brand_input.text(),
            "DuplicateBrand": duplicate_brand_input.text(),
            "ReserveBrand": reserve_brand_input.text(),
            "DesignationHK": designation_hk_input.text(),
            "ApprovalDateHK": approval_date_hk_input.text(),
            "ApprovalPeriodHK": approval_period_hk_input.text(),
            "ManufacturerAbbreviation": manufacturer_abbreviation_input.text(),
            "FilePath": getattr(dialog, 'file_path', '')
        }
        # Путь к вашей базе данных
        db_path = "/home/roman/SQLiteStudio/Naznachenie_db"
        # Создание объекта DatabaseManager
        db_manager = DatabaseManager(db_path)
        try:
            # Подключение к базе данных
            db_manager.connect()
            # Формирование SQL-запроса на вставку данных
            insert_query = f'''
                INSERT INTO TestBd (
                    Name, Engine, CompositeParts, FuelBrand, MainBrand,
                    DuplicateBrand, ReserveBrand, DesignationHK,
                    ApprovalDateHK, ApprovalPeriodHK, ManufacturerAbbreviation,FilePath
                ) VALUES (
                    '{new_data["Name"]}', '{new_data["Engine"]}', '{new_data["CompositeParts"]}',
                    '{new_data["FuelBrand"]}', '{new_data["MainBrand"]}', '{new_data["DuplicateBrand"]}',
                    '{new_data["ReserveBrand"]}', '{new_data["DesignationHK"]}', '{new_data["ApprovalDateHK"]}',
                    '{new_data["ApprovalPeriodHK"]}', '{new_data["ManufacturerAbbreviation"]}', '{new_data["FilePath"]}'
                );
            '''
            # Выполнение SQL-запроса на вставку данных
            db_manager.execute_query(insert_query)
            # Подтверждение изменений
            db_manager.connection.commit()
            # Загрузка обновленных данных в модель
            headers = [
                "Изделие", "Силовая установка (двигатель)", "Составные части комплексного изделия",
                "Марка ГСМ", "Марка Основная", "Марка Дублирующая", "Марка Резервная", "Обозначение ХК",
                "Дата согласования ХК", "Срок согласования ХК", "Предприятие-изготовитель изделия"
            ]
            model = db_manager.load_data_to_model(headers)
            table.setModel(model)
            # Отключение от базы данных
            db_manager.disconnect()
            return model
        except Exception as e:
            print("Ошибка при добавлении данных:", e)
            return None
    else:
        return None
