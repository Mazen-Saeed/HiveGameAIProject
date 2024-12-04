from PyQt5.QtWidgets import QApplication
from Src.start_window import StartWindow
import sys
import os
os.chdir("/home/mazen/PycharmProjects/HiveGame/")

app = QApplication(sys.argv)
start_window = StartWindow()
start_window.show()  # Show the main window

sys.exit(app.exec_())  # Start the main event loop