class CellPosition:
    def __init__(self, q, r):
        """
        Represents a position on the grid.
        :param q: Column value
        :param r: Row value
        """
        self.q = q  # Column value
        self.r = r  # Row value


class GameState:
    def __init__(self, player1Type, player2Type,player1Level,player2Level):
        """
        Initializes the game state.
        :param player1Type: "p" if player 1 is a person, "c" if a computer
        :param player2Type: "p" if player 2 is a person, "c" if a computer
        :param player1Level: "e" for easy, "m" for medium, "h" for hard, "p" if player
        :param player2Level: "e" for easy, "m" for medium, "h" for hard, "p" if player
        """
        self.player1Type = player1Type
        self.player2Type = player2Type
        self.player1Level = player1Level
        self.player2Level = player2Level
        self._initialize_state()

    def _initialize_state(self):
        """
        A helper method to initialize or reset the state of the game.
        Used by both the constructor and reset method.
        """
        self.state = [["" for _ in range(50)] for _ in range(50)]  # Reset grid state
        self.q1 = CellPosition(-1, -1)  # Reset player 1's queen bee position
        self.q2 = CellPosition(-1, -1)  # Reset player 2's queen bee position
        self.turn = 1  # Reset turn to player 1
        self.player1Moves = 0  # Reset player 1's move count
        self.player2Moves = 0  # Reset player 2's move count

    def reset(self):
        """
        Resets the game state to its initial configuration.
        """
        self._initialize_state()


    def make_a_move(self):
        """
        Makes a move for the current player in case of a computer using the AI algorithms.
        should output 2 pairs (from_cell and to_cell)
        """
        pass

    def get_allowed_moves(self):
        """
        Retrieves all allowed moves for the current player.
        Used when a person is playing.
        """
        pass

    def get_allowed_moves_given_a_cell(self, cell):
        """
        Retrieves allowed moves for the specified cell.
        :param cell: An object of CellPosition representing the selected cell
        """
        pass

    def is_this_cell_ok(self,cell):
        """
        checks if the cell the player selected to move the piece in it is ok or not
        """
        pass

    def check_for_a_winning(self):
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
 Ant pieces >> p1, p2
 Spider pieces >> s1, s2
 Beetle pieces >> b1, b2
 Queen pieces >> q1, q2
"""
