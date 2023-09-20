import os
import sys
from glob import glob
from sys import platform

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QApplication, QLabel, QPushButton

from widgets.msg_boxes import WarningMsgBox


class SingleDocProvider:

    def __init__(self, cmbText: str, dirPath: str):
        self.comboBoxText: str = cmbText
        self.dirPath: str = dirPath
        self.files: list[str] = []


class MultiDocProvider:

    def __init__(self, dirPath: str):
        self.docProviders: list[SingleDocProvider] = []
        self.fromDir(dirPath)

    def add(self, sdp: SingleDocProvider):
        self.docProviders.append(sdp)

    def fromDir(self, dirPath: str):
        with os.scandir(dirPath) as files:
            subdir = [file.name for file in files if file.is_dir()]
        for dir in [os.path.join(dirPath, subdir_item) for subdir_item in subdir]:
            sdc = SingleDocProvider(cmbText=os.path.basename(dir),
                                    dirPath=dir)
            sdc.files = glob(os.path.join(dir, "*.docx"))
            self.add(sdc)

    def getComboTexts(self):
        return [sdp.comboBoxText for sdp in self.docProviders]

    def getFilesForMachine(self, machine: str):
        for m in self.docProviders:
            if m.comboBoxText==machine:
                return m.files


class NormTemplateProviderStartWindow(QWidget):

    # def __init__(self, interactor: Interactor):
    def __init__(self,
                 templates_dir_path: str,
                 icons_dir: str):
        super().__init__()
        self.machineryComboBox: QComboBox
        # self.interactor = interactor
        # self.docsProxi: MultiDocProvider = MultiDocProvider(interactor.templates_dir_path)
        self.docsProxi: MultiDocProvider = MultiDocProvider(templates_dir_path)
        self.icons_dir = icons_dir
        self.setUpWindow()

    def setUpWindow(self):
        self.resize(300, 120)
        self.setWindowIcon(QIcon(os.path.join(self.icons_dir, r'cogwheel24.png')))
        self.setWindowTitle('Создание НРГ')

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        topLabel = QLabel('Выберите тип техники')

        openTemplatesBtn = QPushButton('Открыть шаблоны')
        openTemplatesBtn.clicked.connect(self.openTemplate)

        self.machineryComboBox = QComboBox()
        self.machineryComboBox.addItems(self.docsProxi.getComboTexts())

        mainLayout.addWidget(topLabel)
        mainLayout.addWidget(self.machineryComboBox)
        mainLayout.addWidget(openTemplatesBtn)

    def openTemplate(self):
        print(self.docsProxi.getFilesForMachine(self.machineryComboBox.currentText()))
        file_list = ['"{}"'.format(x) for x in self.docsProxi.getFilesForMachine(self.machineryComboBox.currentText())]
        # print('roaoraoraoroaroaro')
        if platform == 'linux':
            # os.system('libreoffice --writer {}'.format(self.docsProxi.getFilesForMachine(self.machineryComboBox.currentText())[0]))
            os.system('libreoffice --writer {}'.format(' '.join(file_list)))
            # print('libreoffice --writer {}'.format(' '.join(file_list)))
        elif platform == 'win32':
            print(file_list)
            # os.system('start {}'.format(' '.join(file_list)))
            # os.system('start "C:\Program Files\ONLYOFFICE\DesktopEditors\DesktopEditors.exe" {}'.format(' '.join(file_list)))
            # print('start "C:\Program Files\ONLYOFFICE\DesktopEditors\DesktopEditors.exe" {}'.format(' '.join(file_list)))
            for f in file_list:
                os.system('start "C:\Program Files\ONLYOFFICE\DesktopEditors\DesktopEditors.exe" {}'.format(f))

        else:
            WarningMsgBox.warning('Невозможно открыть шаблоны документов файл', 'Возможно приложения для открытия '
                                                                                'подобных файлов не настроены или не '
                                                                                'установлены', 'Ошибка')

        # print('[IMPLEMENT ME] opening docx templates...')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    nud = NormTemplateProviderStartWindow(
        templates_dir_path=r'C:\Users\4NR_Operator_34\PycharmProjects\fuels-lubricants-DBMS-2\locals\templates',
        icons_dir=r'C:\Users\4NR_Operator_34\PycharmProjects\fuels-lubricants-DBMS-2\assets\icons')
    nud.show()
    app.exec()
