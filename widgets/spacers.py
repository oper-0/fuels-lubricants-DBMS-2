from PyQt6.QtWidgets import QWidget, QSizePolicy


class HSpacer(QWidget):
    # Custom spacer
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

class VSpacer(QWidget):
    # Custom spacer
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)