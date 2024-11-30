from PyQt5.QtWidgets import QApplication
from Src.start_window import StartWindow
import sys

app = QApplication(sys.argv)
start_window = StartWindow()
app.exec_()


