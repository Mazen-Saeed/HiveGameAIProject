import sys
import math
from functools import partial

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF, QPen, QColor
from PyQt5.QtCore import QPointF , Qt

from Core.cell_position import CellPosition
from Core.game_state import game_state
from GUI.Src.ClickableHexagon import ClickableHexagon
from pieces import Piece, Queen, Ant, Beetle, Grasshopper, Spider

class CustomHexagonalGrid(QGraphicsView):
    def __init__(self, hex_size,parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.hex_size = hex_size
        self.grid_shape = [(row, col) for row in range(50) for col in range(50)]
        self.setRenderHint(0x01)  # Anti-aliasing
        self.draw_custom_grid()
        self.center_on_middle_cell()
        self.state = "waiting" # waiting (default), placement, first_select
        self.selected_tile = None
        self.selected_tile_number = None
        self.selected_hexagon = None
        self.current_player = None

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def create_hexagon(self, center_x, center_y):
        """Creates a hexagon centered at (center_x, center_y)."""
        hexagon = QPolygonF()
        for i in range(6):
            angle_deg = 60 * i - 30  # Flat-top hexagon
            angle_rad = math.radians(angle_deg)
            x = center_x + self.hex_size * math.cos(angle_rad)
            y = center_y + self.hex_size * math.sin(angle_rad)
            hexagon.append(QPointF(x, y))
        return hexagon

    def draw_custom_grid(self):
        """Draws the hexagonal grid based on the provided shape."""
        self.hex_items = {}  # Dictionary to store hexagon instances
        for row, col in self.grid_shape:
            # Calculate hexagon center
            x_offset = col * (self.hex_size * 3.6 / 2)
            y_offset = row * (self.hex_size * math.sqrt(2.5))
            if row % 2 == 1:  # Offset every other column
                x_offset += self.hex_size * math.sqrt(3) / 2

            # Draw the hexagon
            hexagon = self.create_hexagon(x_offset, y_offset)
            hex_item = ClickableHexagon(hexagon,row,col)
            self.scene.addItem(hex_item)
            self.hex_items[(row, col)] = hex_item

    def center_on_middle_cell(self):
        """Centers the viewport on the middle cell (25, 25)."""
        # Calculate the center position of cell (25, 25)
        col = 25
        row = 25
        center_x = col * (self.hex_size * 3.6 / 2)
        center_y = row * (self.hex_size * math.sqrt(2.5))
        if col % 2 == 1:  # Account for offset in odd columns
            center_y += self.hex_size * math.sqrt(3) / 2

        # Center the view on this position
        self.centerOn(center_x, center_y)


    def move_view(self, dx, dy):
        """Moves the view by a specific offset."""
        # Adjust the view position by (dx, dy)
        current_center = self.mapToScene(self.viewport().rect().center())
        new_center = QPointF(current_center.x() + dx, current_center.y() + dy)
        self.centerOn(new_center)


