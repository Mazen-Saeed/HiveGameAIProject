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


        # set style sheet for the application
        with open("Style/gameplay_window.qss", "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        self.disable_buttons()
        # Show our custom UI
        self.show()

    def clicker(self,tile: ClickableLabel):
        if not tile.pressed:
            tile.pressed = True
            tile.setStyleSheet("border: 2px solid aqua;")
        else:
            tile.pressed = False
            tile.setStyleSheet("QLabel { border: 1px solid transparent; } QLabel:hover { border: 2px solid aqua; }")
        print("clicked")

    def creatGrid(self):
        hex_size = 35  # Adjust the size of the hexagons as needed
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


# TODO
# adjust hexagonal shape if border if can be done
# grid of playing
# connect the backend with the GUI


#TODO logic
#1- disable white buttons , disable black buttons, another function to call one of them based on the turn (disableButtons)
