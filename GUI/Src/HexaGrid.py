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
            self.hex_items[(row, col)].signal.polygonClicked.connect(partial(self.handle_hexagon_click, self.hex_items[(row, col)]))

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

    def handle_hexagon_click(self,clicked_hexagon : ClickableHexagon):
        clicked_cell = CellPosition(clicked_hexagon.row,clicked_hexagon.col)
        if self.state == "waiting":
            pass
        elif self.state == "placement":
            piece = None
            if self.selected_tile == "A":
                piece = Ant(self.current_player)
            elif self.selected_tile == "B":
                piece = Beetle(self.current_player)
            elif self.selected_tile == "G":
                piece = Grasshopper(self.current_player)
            elif self.selected_tile == "S":
                piece = Spider(self.current_player)
            elif self.selected_tile == "Q":
                piece = Queen(self.current_player)

            if game_state.is_this_cell_ok(clicked_cell,piece,None):
                self.adjust_cells(None,clicked_cell,piece)
                game_state.update_state(clicked_cell,piece,None)






        elif self.state == "first_select":
            pass
        elif self.state == "second_select":
            pass
        else:
            pass



    def adjust_cells(self, from_cell, to_cell, piece):
        if from_cell != None:
            from_row = from_cell.r
            from_col = from_cell.q
            from_cell_obj = self.hex_items.get((from_row, from_col))
            from_cell_obj.remove_image()

        to_row = to_cell.r
        to_col = to_cell.q
        to_cell_obj = self.hex_items.get((to_row, to_col))
        if piece.name == 'A' and piece.player == 0:
            to_cell_obj.add_image("Images/Black Ant.png")
        elif piece.name == 'A' and piece.player == 1:
            to_cell_obj.add_image("Images/White Ant.png")
        elif piece.name == 'G' and piece.player == 0:
            to_cell_obj.add_image("Images/Black Grasshopper.png")
        elif piece.name == 'G' and piece.player == 1:
            to_cell_obj.add_image("Images/White Grasshopper.png")
        elif piece.name == 'B' and piece.player == 0:
            to_cell_obj.add_image("Images/Black Beetle.png")
        elif piece.name == 'B' and piece.player == 1:
            to_cell_obj.add_image("Images/White Beetle.png")
        elif piece.name == 'S' and piece.player == 0:
            to_cell_obj.add_image("Images/Black Spider.png")
        elif piece.name == 'S' and piece.player == 1:
            to_cell_obj.add_image("Images/White Spider.png")
        elif piece.name == 'Q' and piece.player == 0:
            to_cell_obj.add_image("Images/Black Bee.png")
        elif piece.name == 'Q' and piece.player == 1:
            to_cell_obj.add_image("Images/White Bee.png")


