import math

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QPen, QColor, QPixmap, QPainterPath, QRegion, QBrush, QPainter
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsPixmapItem, QGraphicsItemGroup, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsPathItem


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

    def unmark(self):
        self.setPen(QPen(QColor("transparent"), 2))  # Default border color

    def add_image(self, image_path):
        """Set a scaled image as the brush for the hexagon."""
        pixmap = QPixmap(image_path)

        hex_rect = self.boundingRect()
        # Scale the pixmap to the bounding rectangle of the hexagon
        scaled_pixmap = pixmap.scaled(int(hex_rect.width()), int(hex_rect.height()), Qt.KeepAspectRatioByExpanding,Qt.SmoothTransformation)

        self.image_item = QGraphicsPixmapItem(scaled_pixmap, parent=self)

        # Center the pixmap in the hexagon
        pixmap_center_x = hex_rect.x() + (hex_rect.width() - pixmap.width()) / 2
        pixmap_center_y = hex_rect.y() + (hex_rect.height() - pixmap.height()) / 2
        self.image_item.setPos(pixmap_center_x, pixmap_center_y)

        # Optional: Clip the image to the hexagonal shape
        clip_path = QPainterPath()
        clip_path.addPolygon(self.polygon())  # Use the hexagonal polygon
        self.clip_item = QGraphicsPathItem(clip_path, parent=self)
        self.clip_item.setPen(QPen(Qt.NoPen))

        brush = QBrush(self.image_item.pixmap())
        self.clip_item.setBrush(brush)

        self.image_item.setParentItem(self.clip_item)  # Make the image follow the clip

    def remove_image(self):
        """Remove the image from the hexagon."""
        if hasattr(self, 'image_item') and self.image_item:
            self.scene().removeItem(self.image_item)
            self.image_item = None
        if hasattr(self, 'clip_item') and self.clip_item:
            self.scene().removeItem(self.clip_item)
            self.clip_item = None
