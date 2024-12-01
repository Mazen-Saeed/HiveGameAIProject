from PyQt5.QtWidgets import QApplication
from Src.start_window import StartWindow
from Src.gameplay_window import GameplayWindow
import sys

app = QApplication(sys.argv)
#StartWindow = StartWindow()
GameplayWindow = GameplayWindow()
app.exec_()


