from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QFrame, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys
import os

from GUI.Src.ClickableLabel import ClickableLabel
from GUI.Src.HexaGrid import CustomHexagonalGrid

from Core.game_state import GameState,game_state

class GameplayWindow(QMainWindow):
    def __init__(self):
        super(GameplayWindow, self).__init__()
        # set the Size of the window
        # self.setFixedSize(1917, 1080)
        # load ui file
        print(os.getcwd())  # for debugging
        uic.loadUi("UI/gameplay_window.ui", self)

        self.load_font_needed()

        # catch UI element from ui file
        # Black player tiles
        self.black_ant_1 = self.findChild(ClickableLabel, "black_ant_1")
        self.black_ant_2 = self.findChild(ClickableLabel, "black_ant_2")
        self.black_ant_3 = self.findChild(ClickableLabel, "black_ant_3")
        self.black_grasshopper_1 = self.findChild(ClickableLabel, "black_grasshopper_1")
        self.black_grasshopper_2 = self.findChild(ClickableLabel, "black_grasshopper_2")
        self.black_grasshopper_3 = self.findChild(ClickableLabel, "black_grasshopper_3")
        self.black_beetle_1 = self.findChild(ClickableLabel, "black_beetle_1")
        self.black_beetle_2 = self.findChild(ClickableLabel, "black_beetle_2")
        self.black_spider_1 = self.findChild(ClickableLabel, "black_spider_1")
        self.black_spider_2 = self.findChild(ClickableLabel, "black_spider_2")
        self.black_bee = self.findChild(ClickableLabel, "black_bee")

        # White player tiles
        self.white_ant_1 = self.findChild(ClickableLabel, "white_ant_1")
        self.white_ant_2 = self.findChild(ClickableLabel, "white_ant_2")
        self.white_ant_3 = self.findChild(ClickableLabel, "white_ant_3")
        self.white_grasshopper_1 = self.findChild(ClickableLabel, "white_grasshopper_1")
        self.white_grasshopper_2 = self.findChild(ClickableLabel, "white_grasshopper_2")
        self.white_grasshopper_3 = self.findChild(ClickableLabel, "white_grasshopper_3")
        self.white_beetle_1 = self.findChild(ClickableLabel, "white_beetle_1")
        self.white_beetle_2 = self.findChild(ClickableLabel, "white_beetle_2")
        self.white_spider_1 = self.findChild(ClickableLabel, "white_spider_1")
        self.white_spider_2 = self.findChild(ClickableLabel, "white_spider_2")
        self.white_bee = self.findChild(ClickableLabel, "white_bee")

        #game status label
        self.game_status_label = self.findChild(QLabel, "game_status_label")
        self.game_status_label.setProperty("class", "game_status_label")

        #Grid
        self.grid_placeholder = self.findChild(QFrame, "grid_placeholder")

        self.creatGrid()
        #catch control Buttons
        self.up_button = self.findChild(QPushButton,"up_button")
        self.down_button = self.findChild(QPushButton,"down_button")

        self.right_button = self.findChild(QPushButton, "right_button")
        self.left_button = self.findChild(QPushButton, "left_button")

        #add ctrl button style
        self.up_button.setProperty("class", "ctrl_button")
        self.left_button.setProperty("class", "ctrl_button")
        self.right_button.setProperty("class", "ctrl_button")
        self.down_button.setProperty("class", "ctrl_button")
        # connect signal and slot

        # connect tiles
        self.black_ant_1.clicked.connect(lambda: self.clicker(self.black_ant_1))
        self.white_ant_1.clicked.connect(lambda: self.clicker(self.white_ant_1))
        self.white_ant_2.clicked.connect(lambda: self.clicker(self.white_ant_2))
        self.black_ant_2.clicked.connect(lambda: self.clicker(self.black_ant_2))
        self.black_ant_3.clicked.connect(lambda: self.clicker(self.black_ant_3))
        self.white_ant_3.clicked.connect(lambda: self.clicker(self.white_ant_3))

        self.black_grasshopper_1.clicked.connect(lambda: self.clicker(self.black_grasshopper_1))
        self.black_grasshopper_2.clicked.connect(lambda: self.clicker(self.black_grasshopper_2))
        self.black_grasshopper_3.clicked.connect(lambda: self.clicker(self.black_grasshopper_3))
        self.white_grasshopper_1.clicked.connect(lambda: self.clicker(self.white_grasshopper_1))
        self.white_grasshopper_2.clicked.connect(lambda: self.clicker(self.white_grasshopper_2))
        self.white_grasshopper_3.clicked.connect(lambda: self.clicker(self.white_grasshopper_3))

        self.black_beetle_1.clicked.connect(lambda: self.clicker(self.black_beetle_1))
        self.black_beetle_2.clicked.connect(lambda: self.clicker(self.black_beetle_2))
        self.white_beetle_1.clicked.connect(lambda: self.clicker(self.white_beetle_1))
        self.white_beetle_2.clicked.connect(lambda: self.clicker(self.white_beetle_2))

        self.black_spider_1.clicked.connect(lambda: self.clicker(self.black_spider_1))
        self.black_spider_2.clicked.connect(lambda: self.clicker(self.black_spider_2))
        self.white_spider_1.clicked.connect(lambda: self.clicker(self.white_spider_1))
        self.white_spider_2.clicked.connect(lambda: self.clicker(self.white_spider_2))

        self.black_bee.clicked.connect(lambda: self.clicker(self.black_bee))
        self.white_bee.clicked.connect(lambda: self.clicker(self.white_bee))

        self.start_game()
        # set style sheet for the application
        with open("Style/gameplay_window.qss", "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        # Show our custom UI
        self.show()


    def clicker(self,tile: ClickableLabel):
        allowed_cells = game_state.get_allowed_cells()
        for cell in allowed_cells:
            row = cell.r
            col = cell.q
            self.hex_grid.hex_items.get((row,col)).mark()
        if not tile.pressed:
            tile.pressed = True
            tile.setStyleSheet("border: 2px solid aqua;")
        else:
            tile.pressed = False
            tile.setStyleSheet("QLabel { border: 1px solid transparent; } QLabel:hover { border: 2px solid aqua; }")

    def creatGrid(self):
        hex_size = 52  # Adjust the size of the hexagons as needed
        self.hex_grid = CustomHexagonalGrid(parent=self.grid_placeholder, hex_size=hex_size)

        self.up_button.clicked.connect(lambda: self.hex_grid.move_view(0, -100))
        self.down_button.clicked.connect(lambda: self.hex_grid.move_view(0, 100))
        self.right_button.clicked.connect(lambda: self.hex_grid.move_view(100, 0))
        self.left_button.clicked.connect(lambda: self.hex_grid.move_view(-100, 0))
        layout = QVBoxLayout(self.grid_placeholder)
        layout.addWidget(self.hex_grid)

    def load_font_needed(self):
        font_id = QFontDatabase.addApplicationFont("Fonts/Pridi-SemiBold.ttf")
        if font_id == -1:
            print("Failed to load the font.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            print(f"Loaded font: {font_family}")

    def disable_white_buttons(self):
        self.white_ant_1.disable()
        self.white_ant_2.disable()
        self.white_ant_3.disable()
        self.white_grasshopper_1.disable()
        self.white_grasshopper_2.disable()
        self.white_grasshopper_3.disable()
        self.white_beetle_1.disable()
        self.white_beetle_2.disable()
        self.white_spider_1.disable()
        self.white_spider_2.disable()
        self.white_bee.disable()

    def disable_black_buttons(self):
        self.black_ant_1.disable()
        self.black_ant_2.disable()
        self.black_ant_3.disable()
        self.black_grasshopper_1.disable()
        self.black_grasshopper_2.disable()
        self.black_grasshopper_3.disable()
        self.black_beetle_1.disable()
        self.black_beetle_2.disable()
        self.black_spider_1.disable()
        self.black_spider_2.disable()
        self.black_bee.disable()
    def enable_white_buttons(self):
        self.white_ant_1.enable()
        self.white_ant_2.enable()
        self.white_ant_3.enable()
        self.white_grasshopper_1.enable()
        self.white_grasshopper_2.enable()
        self.white_grasshopper_3.enable()
        self.white_beetle_1.enable()
        self.white_beetle_2.enable()
        self.white_spider_1.enable()
        self.white_spider_2.enable()
        self.white_bee.enable()

    def enable_black_buttons(self):
        self.black_ant_2.enable()
        self.black_ant_3.enable()
        self.black_grasshopper_1.enable()
        self.black_grasshopper_2.enable()
        self.black_grasshopper_3.enable()
        self.black_beetle_1.enable()
        self.black_beetle_2.enable()
        self.black_spider_1.enable()
        self.black_spider_2.enable()
        self.black_bee.enable()

    def disable_buttons(self):
        if game_state.turn == 0 :
            self.disable_white_buttons()
        else:
            self.disable_black_buttons()

    def enable_buttons(self):
        if game_state.turn == 0 :
            self.enable_black_buttons()
        else:
            self.enable_white_buttons()

    def start_game(self):
        while True:
            if(game_state.player_allowed_to_play()):
                self.disable_buttons()
                self.enable_buttons()
                current_turn = game_state.turn
                if game_state.players[current_turn].player_type == 'c':
                    from_cell, to_cell, piece = game_state.make_a_move()
                    ##TODO: make the movement in GUI
                    self.adjust_cells(from_cell,to_cell,piece)
                    print(from_cell, to_cell, piece)
                    game_state.update_state(to_cell, piece, from_cell)
                    game_state.check_for_a_winner()
                else:
                    break
    def adjust_cells(self,from_cell,to_cell,piece):
        if from_cell != None:
            from_row = from_cell.r
            from_col = from_cell.q
            from_cell_obj = self.hex_grid.hex_items.get((from_row,from_col))
            from_cell_obj.remove_image()

        to_row = to_cell.r
        to_col = to_cell.q
        to_cell_obj = self.hex_grid.hex_items.get((to_row,to_col))
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
            to_cell_obj.add_image("Images/Black Queen.png")
        elif piece.name == 'Q' and piece.player == 1:
            to_cell_obj.add_image("Images/White Queen.png")

# TODO
# connect the backend with the GUI


#TODO logic
