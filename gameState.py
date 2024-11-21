class CellPosition:
    def __init__(self, q, r):
        """
        Represents a position on the grid.
        :param q: Column value
        :param r: Row value
        """
        self.q = q  # Column value
        self.r = r  # Row value

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r


class AvailablePieces:
    def __init__(self):
        self.g = 3
        self.a = 3
        self.b = 2
        self.s = 2
        self.q = 1


    def update_available_pieces(self,piece):
        pass


    def is_this_piece_available(self,piece):
        """
        checks if the piece selected to be played is available for the player or no
        """
        pass

class GameState:
    def __init__(self, player1Type, player2Type, player1Level, player2Level):
        self._initialize_state(player1Type, player2Type, player1Level, player2Level)


    def _initialize_state(self,player1Type, player2Type,player1Level,player2Level):
        self.state = [["" for _ in range(50)] for _ in range(50)]  # Reset grid state
        self.q1 = CellPosition(-1, -1)  # Reset player 1's queen bee position
        self.q2 = CellPosition(-1, -1)  # Reset player 2's queen bee position
        self.turn = 1  # Reset turn to player 1
        self.player1Moves = 0  # Reset player 1's move count
        self.player2Moves = 0  # Reset player 2's move count
        self.player1Type = player1Type # "p" if player 1 is a person, "c" if a computer
        self.player2Type = player2Type # "p" if player 2 is a person, "c" if a computer
        self.player1Level = player1Level # "e" for easy, "m" for medium, "h" for hard, "p" if player
        self.player2Level = player2Level # "e" for easy, "m" for medium, "h" for hard, "p" if player
        self.player1AvailablePieces = AvailablePieces()
        self.player2AvailablePieces = AvailablePieces()
        self.current_allowed_moves = []


    def reset(self,player1Type, player2Type,player1Level,player2Level):
        self._initialize_state(player1Type,player2Type,player1Level,player2Level)


    def make_a_move(self):
        """
        Makes a move for the current player in case of a computer using the AI algorithms.
        should output 2 pairs (from_cell and to_cell)
        """
        pass


    def get_allowed_cells(self):
        """
        Retrieves all allowed moves for the current player.
        Used when a person is playing.
        """
        pass


    def must_place_queen_bee(self):
        moves = self.player1Moves
        queen_bee_cell = self.q1
        if self.turn == 2:
            moves = self.player2Moves
            queen_bee_cell = self.q2

        if moves == 3 and queen_bee_cell == CellPosition(-1,-1):
            return True

        return False


    def get_allowed_cells_given_the_piece_on_cell(self, cell):
        """
        Retrieves allowed moves for the specified cell.
        :param cell: An object of CellPosition representing the selected cell
        """
        piece = self.state[cell.r][cell.q]
        if piece.startswith("g"):
            self.get_allowed_cells_for_grasshopper_from_cell(cell)
        elif piece.startswith("a"):
            self.get_allowed_cells_for_ant_from_cell(cell)
        elif piece.startswith("s"):
            self.get_allowed_cells_for_spider_from_cell(cell)
        elif piece.startswith("b"):
            self.get_allowed_cells_for_beetle_from_cell(cell)
        else:
            self.get_allowed_cells_for_queen_bee_from_cell(cell)


    def get_allowed_cells_for_grasshopper_from_cell(self,cell):
        pass

    def get_allowed_cells_for_ant_from_cell(self,cell):
        pass

    def get_allowed_cells_for_spider_from_cell(self,cell):
        pass

    def get_allowed_cells_for_beetle_from_cell(self,cell):
        pass

    def get_allowed_cells_for_queen_bee_from_cell(self,cell):
        pass

    def is_the_piece_on_cell_ok(self,cell):
        """
        checks if the cell the player selected to move the piece in it is ok or not
        """
        pass

    def is_this_cell_ok(self,cell):
        """
         checks if the cell selected to place a piece in it or move a piece to it is from the allowed or not
        """


    def check_for_a_winner(self):
        """
        Checks for a winning condition.
        :return: "p1" if player 1 won, "p2" if player 2 won, or "c" if no player has won
        """
        pass


    def update_state(self, piece, from_cell, to_cell):
        """
        Updates the grid state after a move.
        :param piece: The piece being moved (e.g., "g1", "q2")
        :param from_cell: CellPosition object representing the current position (-1, -1 if the piece wasn't on the grid)
        :param to_cell: CellPosition object representing the target position
        """
        pass




"""
 Pieces in the game:
 Grasshopper pieces >> g1, g2
 Ant pieces >> a1, a2
 Spider pieces >> s1, s2
 Beetle pieces >> b1, b2
 Queen pieces >> q1, q2
"""
