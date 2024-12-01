from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5 import uic
import sys
import os

from GUI.Src.ClickableLabel import ClickableLabel


class GameplayWindow(QMainWindow):
    def __init__(self):
        super(GameplayWindow, self).__init__()

        # load ui file
        print(os.getcwd())  # for debugging
        uic.loadUi("UI/gameplay_window.ui", self)

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
            tile.setStyleSheet("border: 1px solid blue;")
        else:
            tile.pressed = False
            tile.setStyleSheet("QLabel { border: 1px solid transparent; } QLabel:hover { border: 1px solid blue; }")

# TODO
# adjust hexagonal shape if border if can be done
# grid of playing
# connect the backend with the GUI