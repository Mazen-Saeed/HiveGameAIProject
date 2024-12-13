import math

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QPen, QColor, QPixmap, QPainterPath, QRegion, QBrush, QPainter
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsPixmapItem, QGraphicsItemGroup


class ClickableHexagon(QGraphicsPolygonItem):
    """A subclass of QGraphicsPolygonItem to make hexagons clickable."""
    def __init__(self, polygon, row, col, parent=None):
        super().__init__(polygon, parent)
        self.image_item = None
        self.row = row
        self.col = col
        self.setAcceptHoverEvents(True)  # Allow hover events
        self.setPen(QPen(QColor("transparent"), 2))  # Default border color
        self.default_brush = QColor("transparent")
        self.hover_brush = QColor("transparent")
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

    # def hoverEnterEvent(self, event):
    #     """Change appearance on hover."""
    #     if not self.is_selected:
    #         self.setBrush(self.hover_brush)
    #         self.setBrush(QColor("transparent"))
    #         self.setPen(QPen(QColor("transparent"), 2))  # Default border color
    #
    # def hoverLeaveEvent(self, event):
    #     """Revert appearance after hover."""
    #     if not self.is_selected:
    #         self.setBrush(QColor("transparent"))
    #         self.setPen(QPen(QColor("transparent"), 2))  # Default border color

    def mark(self):
        self.setPen(QPen(QColor("cyan"), 2))  # Default border color

    def add_image(self, image_path):
        """Set a scaled image as the brush for the hexagon."""
        pixmap = QPixmap(image_path)
        # Scale the pixmap to the bounding rectangle of the hexagon
        # scaled_pixmap = pixmap.scaled(self.boundingRect().size().toSize())
        scaled_pixmap = pixmap.scaled(int(self.boundingRect().width()), int(self.boundingRect().height())+5, Qt.KeepAspectRatioByExpanding,Qt.SmoothTransformation)

        brush = QBrush(scaled_pixmap)
        self.setBrush(brush)

    def remove_image(self):
        """Remove the image from the hexagon."""
        self.setBrush(self.default_brush)