from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow , QApplication , QLabel ,QPushButton,QFrame
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import uic
import sys
import os

from Core.game_state import GameState,game_state
from GUI.Src.gameplay_window import GameplayWindow


#from gameplay_window import GameplayWindow


class StartWindow(QMainWindow):
    def __init__(self):
        super(StartWindow,self).__init__()

        # self.setFixedSize(1917, 1080)
        self.showMaximized()
        #load ui file
        print(os.getcwd()) # for debugging
        uic.loadUi("UI/start_window.ui",self)


        
        # catch UI element from ui file 
        self.game_label = self.findChild(QLabel,"game_label")
        self.hive_label = self.findChild(QLabel,"hive_label")
        self.hive_photo = self.findChild(QLabel,"hive_photo")
        self.start_game_button = self.findChild(QPushButton,"start_game_button")
        self.exit_button = self.findChild(QPushButton,"exit_button")

        self.player_one_frame = self.findChild(QFrame,"player_one_frame")
        self.player_one_diff_button = self.findChild(QPushButton,"player_one_diff_button")
        self.player_one_label = self.findChild(QLabel,"player_one_label")
        self.player_one_type_button = self.findChild(QPushButton,"player_one_type_button")

        self.player_two_frame = self.findChild(QFrame,"player_two_frame")
        self.player_two_diff_button = self.findChild(QPushButton,"player_two_diff_button")
        self.player_two_label = self.findChild(QLabel,"player_two_label")
        self.player_two_type_button = self.findChild(QPushButton,"player_two_type_button")


        # Load the custom font
        self.load_font_needed()

        # set default data
        self.default_options()

        # Style connection game_options
        self.hive_label.setProperty("class", "hive-label")
        self.game_label.setProperty("class","game-label")
        self.start_game_button.setProperty("class","game_options")
        self.exit_button.setProperty("class","game_options")
        self.player_one_frame.setProperty("class","players_option")
        self.player_two_frame.setProperty("class","players_option")
        self.player_one_label.setProperty("class","players_label")
        self.player_two_label.setProperty("class","players_label")
        self.player_one_type_button.setProperty("class","player_buttons")
        self.player_two_type_button.setProperty("class","player_buttons")
        self.player_one_diff_button.setProperty("class","player_buttons")
        self.player_two_diff_button.setProperty("class","player_buttons")



        # connect signal and slot

        # connect start button action 
        self.start_game_button.clicked.connect(self.start_button_clicked)
        # connect exit button pressed action 
        self.exit_button.clicked.connect(self.exit_clicked)
        # connect player one buttons actions
        self.player_one_diff_button.clicked.connect(self.player_one_diff_func)
        self.player_one_type_button.clicked.connect(self.player_one_type_func)

        # connect player one buttons actions
        self.player_two_diff_button.clicked.connect(self.player_two_diff_func)
        self.player_two_type_button.clicked.connect(self.player_two_type_func)

        #print(os.getcwd()) # for debugging
        # set style sheet for the application
        with open("Style/start_window.qss","r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

        # adjust cursor for all buttons to hand button
        self.set_all_buttons_cursor()
        #Show our custom UI
        self.show()
    

    def start_button_clicked(self):
        # Human -> p
        # AI -> c
        # Easy -> e
        # Medium -> m
        # Difficult -> h
        if(self.player_one_type_button.text() == "Human"):
            self.player_one_type = 'p'
            self.player_one_diff = 'p'
        else:
            self.player_one_type = 'c'
            if self.player_one_diff_button.text() == "Easy":
                self.player_one_diff = 'e'
            elif self.player_one_diff_button.text() == "Medium":
                self.player_one_diff = 'm'
            else:
                self.player_one_diff = 'h'

        if (self.player_two_type_button.text() == "Human"):
            self.player_two_type = 'p'
            self.player_two_diff = 'p'
        else:
            self.player_two_type = 'c'
            if self.player_two_diff_button.text() == "Easy":
                self.player_two_diff = 'e'
            elif self.player_two_diff_button.text() == "Medium":
                self.player_two_diff = 'm'
            else:
                self.player_two_diff = 'h'

        #self.game_state = GameState()

        game_state._initialize_state(self.player_one_type,self.player_two_type,self.player_one_diff,self.player_two_diff)
        self.play_window = GameplayWindow()
        self.play_window.show()
        self.close()

    def exit_clicked(self):
        # kill the program 
         QApplication.quit()

    def load_font_needed(self):
        font_id = QFontDatabase.addApplicationFont("Fonts/Pridi-Medium.ttf")
        if font_id == -1:
            print("Failed to load the font.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            print(f"Loaded font: {font_family}")
    def set_all_buttons_cursor(self):
        # Set hand cursor for all QPushButton instances in the application
        for button in self.findChildren(QPushButton):
            button.setCursor(Qt.PointingHandCursor)
    def player_one_diff_func(self):
        if self.player_one_diff_button.text() == "Easy":
            self.player_one_diff_button.setText("Medium")
        elif self.player_one_diff_button.text() == "Medium":
            self.player_one_diff_button.setText("Difficult")
        elif self.player_one_diff_button.text() == "Difficult":
            self.player_one_diff_button.setText("Easy")

        self.player_one_diff = self.player_one_diff_button.text()




    def player_two_diff_func(self):
        if self.player_two_diff_button.text() == "Easy":
            self.player_two_diff_button.setText("Medium")
        elif self.player_two_diff_button.text() == "Medium":
            self.player_two_diff_button.setText("Difficult")
        elif self.player_two_diff_button.text() == "Difficult":
            self.player_two_diff_button.setText("Easy")

        self.player_two_diff = self.player_two_diff_button.text()



    def player_one_type_func(self):
        if self.player_one_type_button.text() == "AI":
            self.player_one_type_button.setText("Human")
        elif self.player_one_type_button.text() == "Human":
            self.player_one_type_button.setText("AI")

        self.player_one_type = self.player_one_type_button.text()

        if self.player_one_type == "Human":
            self.player_one_diff_button.hide()
        else:
            self.player_one_diff_button.show()



    def player_two_type_func(self):
        if self.player_two_type_button.text() == "AI":
            self.player_two_type_button.setText("Human")
        elif self.player_two_type_button.text() == "Human":
            self.player_two_type_button.setText("AI")

        self.player_two_type = self.player_two_type_button.text()

        if self.player_two_type == "Human":
            self.player_two_diff_button.hide()
        else:
            self.player_two_diff_button.show()


    def default_options(self):
        self.player_one_type = self.player_one_type_button.text()
        self.player_one_diff = self.player_one_diff_button.text()
        self.player_two_diff = self.player_two_diff_button.text()
        self.player_two_type = self.player_two_type_button.text()
        if self.player_one_type == "Human":
            self.player_one_diff_button.hide()
        else:
            self.player_one_diff_button.show()

        if self.player_two_type == "Human":
            self.player_two_diff_button.hide()
        else:
            self.player_two_diff_button.show()




# TODO
# Fix font problem (Done)
# Style Buttons (Done)
# add Ai Options (Done)
# Style Ai Options (Done)
# add logic for Ai action (Done)
# Start BUtton Functionality (Done) except data passed to second window
# Fix directory Functionality