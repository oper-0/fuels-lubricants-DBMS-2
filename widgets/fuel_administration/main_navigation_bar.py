import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import NavigationItemPosition, NavigationToolButton, NavigationPanel


class NavigationBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Инициализация горизонтального макета
        self.hBoxLayout = QHBoxLayout(self)

        # Создание кнопки меню и настройка панели навигации
        self.menuButton = NavigationToolButton(FIF.MENU, self)
        self.navigationPanel = NavigationPanel(parent, True)

        # Установка стиля для NavigationPanel
        self.navigationPanel.setStyleSheet("""
            NavigationPanel {
                background-color: #f1dbf8;
                border: 2px solid #555;
                border-radius: 15px;
            }
        """)

        # Настройка метки заголовка
        self.titleLabel = QLabel(self)

        # Регулировка макета и добавление виджетов
        self.navigationPanel.move(0, 55)
        self.hBoxLayout.setContentsMargins(5, 5, 5, 5)
        self.hBoxLayout.addWidget(self.menuButton)
        self.hBoxLayout.addWidget(self.titleLabel)

        # Подключение сигналов и установка начальных свойств
        self.menuButton.clicked.connect(self.toggleNavigationPanel)
        self.navigationPanel.setExpandWidth(185)
        self.navigationPanel.setMenuButtonVisible(True)
        self.navigationPanel.hide()
        self.navigationPanel.setAcrylicEnabled(True)
        self.window().installEventFilter(self)

    def setTitle(self, title: str):
        # Установка текста метки заголовка и корректировка её размера
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def toggleNavigationPanel(self):
        # Переключение видимости панели навигации и корректировка видимости кнопки меню
        if self.navigationPanel.isVisible():
            self.menuButton.show()
            self.navigationPanel.hide()
        else:
            self.menuButton.hide()
            self.navigationPanel.show()
            self.navigationPanel.raise_()
            self.navigationPanel.expand()

        self.menuButton.show()

    def addItem(self, routeKey, icon, text: str, onClick, selectable=True, position=NavigationItemPosition.TOP):
        # Добавление элемента в панель навигации с обёрткой для события onClick
        def wrapper():
            onClick()
            self.setTitle(text)

        self.navigationPanel.addItem(routeKey, icon, text, wrapper, selectable, position)

    def addSeparator(self, position=NavigationItemPosition.TOP):
        # Добавление разделителя в панель навигации
        self.navigationPanel.addSeparator(position)

    def setCurrentItem(self, routeKey: str):
        # Установка текущего элемента в панели навигации и обновление заголовка
        self.navigationPanel.setCurrentItem(routeKey)
        self.setTitle(self.navigationPanel.widget(routeKey).text())

    def eventFilter(self, obj, e: QEvent):
        # Обработка событий изменения размера окна для корректировки высоты панели навигации
        if obj is self.window():
            if e.type() == QEvent.Type.Resize:
                self.navigationPanel.setFixedHeight(e.size().height() - 600)

        return super().eventFilter(obj, e)


# Основной блок запуска
if __name__ == '__main__':
    # Настройка масштабирования для высокого DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    # Создание экземпляра приложения
    app = QApplication(sys.argv)

    # Создание и отображение NavigationBar
    navigation_bar = NavigationBar()
    navigation_bar.show()

    # Запуск цикла событий приложения
    sys.exit(app.exec())
