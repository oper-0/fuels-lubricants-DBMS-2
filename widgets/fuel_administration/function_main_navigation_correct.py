import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox


# Обработчик коррекции данных
def correct_data_handler(table, cursor, connection, column_mapping):
    # Получение выделенного индекса
    selected_index = table.selectedIndexes()

    # Проверка наличия выделенного индекса
    if not selected_index:
        QMessageBox.warning(table, "Не выбрано", "Пожалуйста, выберите строку для редактирования.")
        return

    # Получение номера строки и столбца
    row = selected_index[0].row()
    column = selected_index[0].column()

    # Получение имени столбца и английского эквивалента
    column_name = table.model().headerData(column, Qt.Orientation.Horizontal)
    english_column_name = column_mapping.get(column_name, column_name)

    # Получение старых данных
    old_data = table.model().index(row, column).data()

    # Ввод новых данных с использованием диалогового окна
    edit_dialog = QDialog(table)
    edit_dialog.setWindowTitle("Редактирование данных")

    layout = QVBoxLayout(edit_dialog)
    layout.addWidget(QLabel(f"{column_name}:"))
    # Set background image for the entire dialog
    edit_dialog.setStyleSheet(
        "background-image: url('assets/icons/background_navigation_correct.png'); background-position: center; "
        "background-repeat: no-repeat;")

    new_data_input = QLineEdit(edit_dialog)
    new_data_input.setText(old_data)
    layout.addWidget(new_data_input)

    # Создаем горизонтальную компоновку только для кнопок
    button_layout = QHBoxLayout()

    ok_button = QPushButton("OK", edit_dialog)
    ok_button.setStyleSheet("""
        QPushButton {
            background-color: #f1dbf8;
            border: 3px solid #555;
            border-radius: 15px;
        }
    """)
    ok_button.setFixedSize(150, 40)
    ok_button.clicked.connect(edit_dialog.accept)
    button_layout.addWidget(ok_button)

    cancel_button = QPushButton("Отмена", edit_dialog)
    cancel_button.setStyleSheet("""
        QPushButton {
            background-color: #f1dbf8;
            border: 3px solid #555;
            border-radius: 15px;
        }
    """)
    cancel_button.setFixedSize(150, 40)
    cancel_button.clicked.connect(edit_dialog.reject)
    button_layout.addWidget(cancel_button)

    layout.addLayout(button_layout)

    result = edit_dialog.exec()

    if result == QDialog.DialogCode.Accepted:
        new_data = new_data_input.text()

        try:
            # Получение значения 'DesignationHK'
            designation_hk = table.model().index(row, 7).data()

            # Выполнение SQL-запроса на обновление данных
            update_query = f"UPDATE TestBd SET `{english_column_name}` = ? WHERE DesignationHK = ?;"
            cursor.execute(update_query, (new_data, designation_hk))
            connection.commit()

            # Обновление конкретного элемента в модели
            item = table.model().item(row, column)
            if item:
                item.setText(new_data)

            # Фильтрация данных в заголовке таблицы
            table.horizontalHeader().filter_data()

            # Вывод информационного сообщения об успешном обновлении данных
            QMessageBox.information(table, "Данные обновлены", f"{column_name}")
        except sqlite3.Error as e:
            # Вывод сообщения об ошибке при обновлении данных
            QMessageBox.critical(table, "Ошибка", "Произошла ошибка при обновлении данных.")
