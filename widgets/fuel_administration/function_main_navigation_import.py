import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout


def import_data_handler(connection, cursor):
    # Step 1: User selects the file
    file_dialog = QFileDialog()
    file_dialog.setOption(QFileDialog.Option.ReadOnly, True)
    file_dialog.setWindowTitle("Выберите файл для импорта")
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    file_dialog.setNameFilter("Text Files (*.txt);;CSV Files (*.csv);;All Files (*)")

    if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
        selected_file = file_dialog.selectedFiles()[0]

        # Step 2: Show dialog to get DesignationHK and FilePath
        data_input_dialog = DataInputDialog()
        if data_input_dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                # Obtain DesignationHK and FilePath from the dialog
                designation_hk, file_path = data_input_dialog.get_data()

                with open(selected_file, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if not lines:
                        raise ValueError("Данные не найдены в выбранном файле.")

                    # Identify header dynamically
                    header = lines[0].strip().split(',')
                    if len(header) != 11:
                        raise ValueError("Некорректный формат заголовка. Пропускаем файл.")

                    for line in lines[1:]:
                        data = line.strip().split(',')

                        # Use values obtained from the dialog
                        data_dict = {header[i]: data[i] if i < len(data) else '' for i in range(len(header))}
                        data_dict['DesignationHK'] = designation_hk
                        data_dict['FilePath'] = file_path

                        # Insert data into the database
                        insert_query = '''
                                   INSERT INTO TestBd (
                                       Name, Engine, CompositeParts, FuelBrand, MainBrand,
                                       DuplicateBrand, ReserveBrand, DesignationHK,
                                       ApprovalDateHK, ApprovalPeriodHK, ManufacturerAbbreviation, FilePath
                                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                               '''
                        cursor.execute(insert_query, tuple(data_dict.values()))
                connection.commit()
            except ValueError as ve:
                print(f"Ошибка при импорте данных: {ve}")
                # Handle the rest of the exceptions as needed
            except Exception as e:
                print(f"Ошибка при импорте данных: {e}")


class DataInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set up your dialog UI components
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        designation_hk_label = QLabel("DesignationHK:")
        self.designation_hk_input = QLineEdit()

        file_button = QPushButton("Выбрать файл")
        file_button.setStyleSheet("""
            QPushButton {
                background-color: #f1dbf8;
                border: 3px solid #555;
            }
        """)
        file_button.setFixedSize(350, 30)
        file_button.clicked.connect(self.on_file_button_clicked)

        common_button_style = """
            QPushButton {
                background-color: #f1dbf8;
                border: 3px solid #555;
                border-radius: 15px;
            }
        """

        ok_button = QPushButton("ОК")
        ok_button.setStyleSheet(common_button_style)
        ok_button.setFixedSize(150, 40)
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet(common_button_style)
        cancel_button.setFixedSize(150, 40)
        cancel_button.clicked.connect(self.reject)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addWidget(designation_hk_label)
        layout.addWidget(self.designation_hk_input)
        layout.addWidget(file_button)
        layout.addLayout(button_layout)

        # Set the background image for the dialog
        background_label = QLabel(self)
        background_label.setPixmap(QPixmap("assets/icons/background_navigation_add.jpg"))
        background_label.setGeometry(0, 0, 800, 600)

        self.setLayout(layout)

    def on_file_button_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл", "", "All Files (*)")

        if file_path:
            filename_without_extension, _ = os.path.splitext(os.path.basename(file_path))
            self.designation_hk_input.setText(filename_without_extension)
            self.file_path = file_path

    def get_data(self):
        designation_hk = self.designation_hk_input.text()
        file_path = getattr(self, 'file_path', None)
        return designation_hk, file_path
