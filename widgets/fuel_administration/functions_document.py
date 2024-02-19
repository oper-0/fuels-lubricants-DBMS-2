import subprocess
import platform
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QMenu, QMessageBox


def show_context_menu(parent, file_path):
    context_menu = QMenu(parent)
    view_action = QAction("Просмотр документа", parent)
    view_action.triggered.connect(lambda: open_file(file_path))
    add_to_document_action = QAction("Добавить в сводный документ", parent)
    # Add event
    context_menu.addAction(view_action)
    context_menu.addAction(add_to_document_action)
    # Получаем текущую позицию курсора
    cursor_pos = QCursor.pos()
    # Создаем новую точку с учетом смещения по горизонтали
    new_pos = cursor_pos + QPoint(20, 0)
    context_menu.exec(new_pos)


def open_file(file_path):
    system = platform.system()
    try:
        if system == "Linux":
            subprocess.run(['xdg-open', file_path])
        elif system == "Darwin":
            subprocess.run(['open', file_path])
        elif system == "Windows":
            subprocess.run(['start', '', file_path], shell=True)
        else:
            print("Unsupported operating system")
    except Exception as e:
        print("Error opening file:", e)
        show_warning("Ошибка открытия документа!", f"Проверьте установлено ли программное обеспечение,а также "
                                                   f"наличие документа в базе.  \n{e}")


def show_warning(title, message):
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Icon.Warning)
    warning.setWindowTitle(title)
    warning.setText(message)
    warning.exec()
