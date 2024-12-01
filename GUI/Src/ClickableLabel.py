from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Define a custom signal

    pressed = False
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_shadow()

    def init_shadow(self):
        # Create a shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setOffset(10, 10)  # Shadow offset
        shadow.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black
        self.setGraphicsEffect(shadow)


    def mousePressEvent(self, event):
        # Emit the clicked signal when the label is clicked
        self.clicked.emit()
        super().mousePressEvent(event)
