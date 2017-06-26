from PyQt5.QtWidgets import QLabel

class SaveLabel(QLabel):
    def __init__(self, parent=None, ):
        super(SaveLabel, self).__init__(parent)
        self.is_save = False

    def mousePressEvent(self, e):
        self.is_save = True
        print("sata")