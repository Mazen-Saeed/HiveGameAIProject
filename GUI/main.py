from PyQt5.QtWidgets import QApplication
from Src.start_window import StartWindow
from Src.gameplay_window import GameplayWindow
import sys
import os
#os.chdir("/home/mazen/PycharmProjects/HiveGame/")

app = QApplication(sys.argv)
StartWindow = StartWindow()
#GameplayWindow = GameplayWindow()
app.exec_()


