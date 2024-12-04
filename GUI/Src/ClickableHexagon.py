import math

from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsPolygonItem


class ClickableHexagon(QGraphicsPolygonItem):
    """A subclass of QGraphicsPolygonItem to make hexagons clickable."""
    def __init__(self, polygon, row, col, parent=None):
        super().__init__(polygon, parent)
        self.row = row
        self.col = col
        self.setAcceptHoverEvents(True)  # Allow hover events
        self.setPen(QPen(QColor("transparent"), 2))  # Default border color
        self.default_brush = QColor("white")
        self.hover_brush = QColor("lightblue")
        self.selected_brush = QColor("yellow")
        self.is_selected = False

    def mousePressEvent(self, event):
        """Handle click events."""
        if not self.is_selected:
            self.is_selected = True
            self.setBrush(self.selected_brush)
            print(f"Hexagon at ({self.row}, {self.col}) selected")
        else:
            self.is_selected = False
            self.setBrush(self.default_brush)
            print(f"Hexagon at ({self.row}, {self.col}) deselected")

    def hoverEnterEvent(self, event):
        """Change appearance on hover."""
        if not self.is_selected:
            self.setBrush(self.hover_brush)
            self.setBrush(QColor("cyan"))
            self.setPen(QPen(QColor("cyan"), 2))  # Default border color

    def hoverLeaveEvent(self, event):
        """Revert appearance after hover."""
        if not self.is_selected:
            self.setBrush(QColor("transparent"))
            self.setPen(QPen(QColor("cyan"), 2))  # Default border color