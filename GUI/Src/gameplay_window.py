from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QFrame, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import uic
import sys
import os

from GUI.Src.ClickableLabel import ClickableLabel
from GUI.Src.HexaGrid import CustomHexagonalGrid


class GameplayWindow(QMainWindow):
    def __init__(self):
        super(GameplayWindow, self).__init__()

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
        # connect signal and slot

        # connect tiles
        self.black_ant_1.clicked.connect(lambda: self.clicker(self.black_ant_1))

        # set style sheet for the application
        with open("Style/gameplay_window.qss", "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        # Show our custom UI
        self.show()

    def clicker(self,tile: ClickableLabel):
        if not tile.pressed:
            tile.pressed = True
            tile.setStyleSheet("border: 2px solid aqua;")
        else:
            tile.pressed = False
            tile.setStyleSheet("QLabel { border: 1px solid transparent; } QLabel:hover { border: 2px solid aqua; }")

    def creatGrid(self):
        hex_size = 35  # Adjust the size of the hexagons as needed
        self.hex_grid = CustomHexagonalGrid(parent=self.grid_placeholder, hex_size=hex_size)

        layout = QVBoxLayout(self.grid_placeholder)
        layout.addWidget(self.hex_grid)

    def load_font_needed(self):
        font_id = QFontDatabase.addApplicationFont("Fonts/Pridi-SemiBold.ttf")
        if font_id == -1:
            print("Failed to load the font.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            print(f"Loaded font: {font_family}")

# TODO
# adjust hexagonal shape if border if can be done
# grid of playing
# connect the backend with the GUI