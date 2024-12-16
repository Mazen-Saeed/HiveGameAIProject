from functools import partial

from PyQt5.QtCore import QTimer, QUrl, QCoreApplication
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QSoundEffect
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QFrame, QVBoxLayout, QApplication
from PyQt5.QtGui import QFontDatabase
from PyQt5 import uic
import os

from GUI.Src.ClickableHexagon import ClickableHexagon
from GUI.Src.ClickableLabel import ClickableLabel
from GUI.Src.HexaGrid import CustomHexagonalGrid

from Core.game_state import game_state
from GUI.Src.utils import resource_path
from pieces import Ant, Beetle, Grasshopper, Spider, Queen


class GameplayWindow(QMainWindow):
    def __init__(self):
        super(GameplayWindow, self).__init__()
        # set the Size of the window
        # self.setFixedSize(1917, 1080)
        # self.showMaximized()
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)  # Set the window geometry to the screen size

        # Optional: Set full-screen mode
        self.showFullScreen()  # Makes the window full screen
        # load ui file
        print(os.getcwd())  # for debugging
        ui_file = resource_path("UI/gameplay_window.ui")
        uic.loadUi(ui_file, self)

        self.styleSheet()
        self.load_font_needed()

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.start_turn)


        # catch UI element from ui file
        self.catch_UI_elements()
        self.creatGrid()
        self.connect_grid()
        self.init_tiles()
        # connect signal and slot
        # connect tiles
        self.connect_tiles()
        self.start_turn()

        # set style sheet for the application
        game_window_qss = resource_path("Style/gameplay_window.qss")
        with open(game_window_qss, "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        # Show our custom UI
        self.show()

    def start_timer(self):
        self.game_timer.start(1000)

    def clicker(self,tile: ClickableLabel):
        allowed_cells = game_state.get_allowed_cells()
        if not tile.pressed:
            self.hex_grid.state = "placement"
            self.hex_grid.selected_tile = tile.type
            self.hex_grid.current_player = tile.player
            self.hex_grid.selected_tile_number = tile.number

            for cell in allowed_cells:
                row = cell.r
                col = cell.q
                self.hex_grid.hex_items.get((row, col)).mark()
            tile.pressed = True
            tile.setStyleSheet("border: 2px solid aqua;")
        else:
            self.hex_grid.state = "waiting"
            self.hex_grid.selected_tile = None
            self.hex_grid.current_player = None
            self.hex_grid.selected_tile_number = None
            for cell in allowed_cells:
                row = cell.r
                col = cell.q
                self.hex_grid.hex_items.get((row, col)).unmark()
            tile.pressed = False
            tile.setStyleSheet("QLabel { border: 1px solid transparent; } QLabel:hover { border: 2px solid aqua; }")

    def creatGrid(self):
        hex_size = 50  # Adjust the size of the hexagons as needed
        self.hex_grid = CustomHexagonalGrid(parent=self.grid_placeholder, hex_size=hex_size)
        self.up_button.clicked.connect(lambda: self.hex_grid.move_view(0, -100))
        self.down_button.clicked.connect(lambda: self.hex_grid.move_view(0, 100))
        self.right_button.clicked.connect(lambda: self.hex_grid.move_view(100, 0))
        self.left_button.clicked.connect(lambda: self.hex_grid.move_view(-100, 0))
        layout = QVBoxLayout(self.grid_placeholder)
        layout.addWidget(self.hex_grid)

    def load_font_needed(self):
        load_font = resource_path("Fonts/Pridi-SemiBold.ttf")
        font_id = QFontDatabase.addApplicationFont(load_font)
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
        self.black_ant_3.enable()
        self.black_ant_1.enable()
        self.black_ant_2.enable()
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

    def start_turn(self):
        self.disable_buttons()
        self.enable_buttons()
        if(game_state.player_allowed_to_play()):
            current_turn = game_state.turn
            if game_state.players[current_turn].player_type == 'c':
                self.ai_turn()

            else:
                self.game_timer.stop()
                self.player_turn()

        self.adjust_game_label()
        state = game_state.check_for_a_winner()
        if state != -1:
            self.winning_label_show(state)
            print("game finished")
            self.game_timer.stop()

    def ai_turn(self):
        self.start_timer()
        from_cell, to_cell, piece = game_state.make_a_move()
        self.adjust_cells(from_cell, to_cell, piece)
        print(from_cell, to_cell, piece)
        game_state.update_state(to_cell, piece, from_cell)
        state = game_state.check_for_a_winner()
        if state != -1:
            self.winning_label_show(state)
            print("game finished")
            self.game_timer.stop()

    def player_turn(self):
        test = game_state.must_place_queen_bee()
        if game_state.must_place_queen_bee():
            self.queen_must_play()

        #self.start_timer()


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
            load_image = resource_path("Images/Black Ant.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'A' and piece.player == 1:
            load_image = resource_path("Images/White Ant.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'G' and piece.player == 0:
            load_image = resource_path("Images/Black Grasshopper.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'G' and piece.player == 1:
            load_image = resource_path("Images/White Grasshopper.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'B' and piece.player == 0:
            load_image = resource_path("Images/Black Beetle.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'B' and piece.player == 1:
            load_image = resource_path("Images/White Beetle.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'S' and piece.player == 0:
            load_image = resource_path("Images/Black Spider.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'S' and piece.player == 1:
            load_image = resource_path("Images/White Spider.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'Q' and piece.player == 0:
            load_image = resource_path("Images/Black Bee.png")
            to_cell_obj.add_image(load_image)
        elif piece.name == 'Q' and piece.player == 1:
            load_image = resource_path("Images/White Bee.png")
            to_cell_obj.add_image(load_image)
        self.play_sound()
    def play_sound(self):
        self.sound_effect = QSoundEffect()
        load_sound = resource_path("Sounds/move_sound.wav")
        self.sound_effect.setSource(QUrl.fromLocalFile(load_sound))  # Use absolute path if necessary
        self.sound_effect.setVolume(1.0)
        self.sound_effect.play()


    def catch_UI_elements(self):
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

            # game status label
            self.game_status_label = self.findChild(QLabel, "game_status_label")
            self.game_status_label.setProperty("class", "game_status_label")

            # Grid
            self.grid_placeholder = self.findChild(QFrame, "grid_placeholder")

            # catch control Buttons
            self.up_button = self.findChild(QPushButton, "up_button")
            self.down_button = self.findChild(QPushButton, "down_button")

            self.right_button = self.findChild(QPushButton, "right_button")
            self.left_button = self.findChild(QPushButton, "left_button")

            # add ctrl button style
            self.up_button.setProperty("class", "ctrl_button")
            self.left_button.setProperty("class", "ctrl_button")
            self.right_button.setProperty("class", "ctrl_button")
            self.down_button.setProperty("class", "ctrl_button")
            # add control buttons (reset - home)
            self.home_button = self.findChild(QPushButton,"home_button")
            self.restart_button = self.findChild(QPushButton,"restart_button")
            self.home_button.clicked.connect(self.home_page_reload)
            self.restart_button.clicked.connect(self.restart_page_reload)
    def home_page_reload(self):

        from GUI.Src.start_window import StartWindow
        self.start_window = StartWindow()
        self.start_window.showFullScreen()  # Show the new window fullscreen
        self.close()  # Close the current window


    def restart_page_reload(self):
        game_state.reset(game_state.players[0].player_type,game_state.players[1].player_type,game_state.players[0].player_level,game_state.players[0].player_level)
        """Replace the current window with a new one."""
        self.new_window = GameplayWindow()  # Create a new instance
        self.new_window.showFullScreen()  # Show the new window fullscreen
        self.close()  # Close the current window

    def connect_tiles(self):
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

    def adjust_game_label(self):
        if game_state.turn == 0:
            self.game_status_label.setText("Black Player Turn")
        else:
            self.game_status_label.setText("White Player Turn")
    def queen_must_play(self):
        if game_state.turn == 0:
            self.disable_black_buttons()
            self.black_bee.enable()
        else:
            self.disable_white_buttons()
            self.white_bee.enable()

    def init_black_tiles(self):
        self.black_ant_1.player = 0
        self.black_ant_2.player = 0
        self.black_ant_3.player = 0
        self.black_grasshopper_1.player = 0
        self.black_grasshopper_2.player = 0
        self.black_grasshopper_3.player = 0
        self.black_beetle_1.player = 0
        self.black_beetle_2.player = 0
        self.black_spider_1.player = 0
        self.black_spider_2.player = 0
        self.black_bee.player = 0

        self.black_ant_1.type = "A"
        self.black_ant_2.type = "A"
        self.black_ant_3.type = "A"
        self.black_grasshopper_1.type = "G"
        self.black_grasshopper_2.type = "G"
        self.black_grasshopper_3.type = "G"
        self.black_beetle_1.type = "B"
        self.black_beetle_2.type = "B"
        self.black_spider_1.type = "S"
        self.black_spider_2.type = "S"
        self.black_bee.type = "Q"

        self.black_ant_1.number = 1
        self.black_ant_2.number = 2
        self.black_ant_3.number = 3
        self.black_grasshopper_1.number = 1
        self.black_grasshopper_2.number = 2
        self.black_grasshopper_3.number = 3
        self.black_beetle_1.number = 1
        self.black_beetle_2.number = 2
        self.black_spider_1.number = 1
        self.black_spider_2.number = 2
        self.black_bee.number = 1

    def init_white_tiles(self):
        self.white_ant_1.player = 1
        self.white_ant_2.player = 1
        self.white_ant_3.player = 1
        self.white_grasshopper_1.player = 1
        self.white_grasshopper_2.player = 1
        self.white_grasshopper_3.player = 1
        self.white_beetle_1.player = 1
        self.white_beetle_2.player = 1
        self.white_spider_1.player = 1
        self.white_spider_2.player = 1
        self.white_bee.player = 1
        self.white_ant_1.type = "A"
        self.white_ant_2.type = "A"
        self.white_ant_3.type = "A"
        self.white_grasshopper_1.type = "G"
        self.white_grasshopper_2.type = "G"
        self.white_grasshopper_3.type = "G"
        self.white_beetle_1.type = "B"
        self.white_beetle_2.type = "B"
        self.white_spider_1.type = "S"
        self.white_spider_2.type = "S"
        self.white_bee.type = "Q"

        self.white_ant_1.number = 1
        self.white_ant_2.number = 2
        self.white_ant_3.number = 3
        self.white_grasshopper_1.number = 1
        self.white_grasshopper_2.number = 2
        self.white_grasshopper_3.number = 3
        self.white_beetle_1.number = 1
        self.white_beetle_2.number = 2
        self.white_spider_1.number = 1
        self.white_spider_2.number = 2
        self.white_bee.number = 1

    def init_tiles(self):
        self.init_black_tiles()
        self.init_white_tiles()

    def connect_grid(self):
        for row, col in self.hex_grid.hex_items:
            self.hex_grid.hex_items[(row, col)].signal.polygonClicked.connect(partial(self.handle_hexagon_click, self.hex_grid.hex_items[(row, col)]))

    def handle_hexagon_click(self, clicked_hexagon : ClickableHexagon):
        clicked_cell = game_state.state[clicked_hexagon.row][clicked_hexagon.col]
        if self.hex_grid.state == "waiting":
            if game_state.is_the_piece_on_cell_ok(clicked_cell):
                self.hex_grid.state = "first_select"
                self.hex_grid.selected_hexagon = clicked_hexagon
                clicked_hexagon.is_selected = True
                allowed_cells = game_state.get_allowed_cells_given_the_piece_on_cell(clicked_cell)
                if allowed_cells is not None:
                    for cell in allowed_cells:
                        row = cell.r
                        col = cell.q
                        self.hex_grid.hex_items.get((row, col)).mark()

        elif self.hex_grid.state == "placement":
            piece = None
            if self.hex_grid.selected_tile == "A":
                piece = Ant(self.hex_grid.current_player)
            elif self.hex_grid.selected_tile == "B":
                piece = Beetle(self.hex_grid.current_player)
            elif self.hex_grid.selected_tile == "G":
                piece = Grasshopper(self.hex_grid.current_player)
            elif self.hex_grid.selected_tile == "S":
                piece = Spider(self.hex_grid.current_player)
            elif self.hex_grid.selected_tile == "Q":
                piece = Queen(self.hex_grid.current_player)

            if game_state.is_this_cell_ok(clicked_cell,piece,None):
                self.hex_grid.state = "waiting"
                allowed_cells = game_state.get_allowed_cells()
                for cell in allowed_cells:
                    row = cell.r
                    col = cell.q
                    self.hex_grid.hex_items.get((row, col)).unmark()

                self.adjust_cells(None,clicked_cell,piece)
                game_state.update_state(clicked_cell,piece,None)
                state = game_state.check_for_a_winner()
                if state != -1:
                    self.winning_label_show(state)
                    print("game finished")
                else:
                    self.start_turn()


        elif self.hex_grid.state == "first_select":
            self.hex_grid.state = "waiting"
            if clicked_hexagon.is_selected:
                self.hex_grid.selected_hexagon = None
                clicked_hexagon.is_selected = False
                allowed_cells = game_state.get_allowed_cells_given_the_piece_on_cell(clicked_cell)
                if allowed_cells is not None:
                    for cell in allowed_cells:
                        row = cell.r
                        col = cell.q
                        self.hex_grid.hex_items.get((row, col)).unmark()
            else:
                from_cell_hexagon = self.hex_grid.selected_hexagon
                from_cell =  game_state.state[from_cell_hexagon.row][from_cell_hexagon.col]

                if game_state.is_this_cell_ok(clicked_cell, None,from_cell):
                    allowed_cells = game_state.get_allowed_cells_given_the_piece_on_cell(from_cell)
                    if allowed_cells is not None:
                        for cell in allowed_cells:
                            row = cell.r
                            col = cell.q
                            self.hex_grid.hex_items.get((row, col)).unmark()

                    piece = from_cell.get_top_piece()
                    self.adjust_cells(from_cell, clicked_cell, piece)
                    game_state.update_state(clicked_cell, None, from_cell)
                    state = game_state.check_for_a_winner()
                    if state != -1:
                        self.winning_label_show(state)
                        print("game finished")
                    else:
                        self.start_turn()


        elif self.hex_grid.state == "second_select":
            pass
        else:
            pass
    def winning_label_show(self,state):
        if state == 0:
            self.game_status_label.setText("Black Player Won")
        elif state == 1:
            self.game_status_label.setText("White Player Won")
        elif state == 2 :
            self.game_status_label.setText("Draw")
        # Process events to force the label to update immediately
        QCoreApplication.processEvents()
        self.disable_buttons()



# TODO
# connect the backend with the GUI


#TODO logic
# calling player start timer for start turn