from PyQt5.QtWidgets import QMainWindow , QApplication , QLabel ,QPushButton 
from PyQt5.QtGui import QFont
from PyQt5 import uic
import sys
import os

class StartWindow(QMainWindow):
    def __init__(self):
        super(StartWindow,self).__init__()

        #load ui file
        # print(os.getcwd()) # for debugging 
        uic.loadUi("../UI/start_window.ui",self)


        
        # catch UI element from ui file 
        self.game_label = self.findChild(QLabel,"game_label")
        self.hive_label = self.findChild(QLabel,"hive_label")
        self.hive_photo = self.findChild(QLabel,"hive_photo")
        self.start_game_button = self.findChild(QPushButton,"start_game_button")
        self.exit_button = self.findChild(QPushButton,"exit_button")

        # connect signal and slot

        # connect start button action 
        self.start_game_button.clicked.connect(self.start_button_clicked)
        # connect exit button pressed action 
        self.exit_button.clicked.connect(self.exit_clicked)


        print(os.getcwd()) # for debugging
        # set style sheet for the application
        with open("../Style/start_window.qss","r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

        #Show our custom UI
        self.show()
    

    def start_button_clicked(self):
        # TODO
        pass

    def exit_clicked(self):
        # kill the program 
         QApplication.quit()


# TODO
# Fix font problem
# Style Buttons
# add Ai Options
# Start BUtton Functionality