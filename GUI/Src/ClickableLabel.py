from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PyQt5.QtCore import pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Define a custom signal

    pressed = False
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_shadow()
        self.is_enabled = True
        self.playable = True
        self.type = None
        self.player = None
        self.number = None

    def init_shadow(self):
        # Create a shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setOffset(10, 10)  # Shadow offset
        shadow.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black
        self.setGraphicsEffect(shadow)

    def enable(self):
        """Enable the label to be clicked again and restore opacity."""
        if self.playable:
            self._is_enabled = True
            self.setGraphicsEffect(None)  # Remove opacity effect

    def disable(self):
        """Disable the label from being clicked and reduce opacity."""
        self._is_enabled = False
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)  # Set opacity to 50%
        self.setGraphicsEffect(opacity_effect)

    def mousePressEvent(self, event):
        # Emit the clicked signal when the label is clicked
        if self.is_enabled:
            self.clicked.emit()
            super().mousePressEvent(event)
        else:
            event.ignore()
