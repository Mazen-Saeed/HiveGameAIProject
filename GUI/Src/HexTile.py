from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QPolygon, QRegion
from PyQt5.QtWidgets import QLabel


class HexTile(QLabel):
    clicked = pyqtSignal(tuple)  # Signal to emit the tile's position (row, col)

    def __init__(self, parent=None, hex_size=50, color=QColor("white"), position=None):
        super().__init__(parent)
        self.hex_size = hex_size
        self.color = color
        self.position = position  # Position of the tile (row, col)
        self.set_hexagonal_mask()

    def set_hexagonal_mask(self):
        """Set a hexagonal mask for the tile."""
        w, h = self.width(), self.height()
        hexagon = QPolygon([
            QPoint(w // 2, 0),  # Top center
            QPoint(w, h // 4),  # Top right
            QPoint(w, 3 * h // 4),  # Bottom right
            QPoint(w // 2, h),  # Bottom center
            QPoint(0, 3 * h // 4),  # Bottom left
            QPoint(0, h // 4),  # Top left
        ])
        self.setMask(QRegion(hexagon))

    def paintEvent(self, event):
        """Paint the hexagonal tile."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.setPen(QColor("black"))  # Border color
        painter.drawPolygon(self.mask().toPolygon())

    def mousePressEvent(self, event):
        """Handle click event."""
        self.clicked.emit(self.position)  # Emit the position when clicked
        super().mousePressEvent(event)
