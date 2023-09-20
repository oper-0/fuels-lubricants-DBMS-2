from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QApplication, QStyle


class WarningMsgBox:

    @staticmethod
    def warning(main_text: str, info_text: str, win_title: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowIcon(QIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)))
        msg.setText(main_text)
        msg.setInformativeText(info_text)
        msg.setWindowTitle(win_title)
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.show()
        return_value = msg.exec()
        if return_value == QMessageBox.StandardButton.Ok:
            msg.close()
        return
