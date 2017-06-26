from PyQt5.QtWidgets import QLabel

class CleanLabel(QLabel):
    def __init__(self, parent=None, ):
        super(CleanLabel, self).__init__(parent)
        self.is_clean = False

    def mousePressEvent(self, e):
        self.is_clean = True
