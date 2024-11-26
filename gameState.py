class CellPosition:
    dq = [0, 1, 1, 1, 0, -1]
    dr = [-1, -1, 0, 1, 1, 0]
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

    def get_neighbors(self):
        """
        Returns the neighboring CellPosition objects for the current position.
        """
        neighbors = []
        for i in range(len(CellPosition.dq)):  # Loop over the direction offsets
            new_q = self.q + CellPosition.dq[i]
            new_r = self.r + CellPosition.dr[i]
            neighbors.append(CellPosition(new_q, new_r))

        return neighbors

class Piece:
    def __init__(self,name,player):
        self.name = name
        self.player = player

    def get_name(self):
        return self.name

    def get_player(self):
        return self.player


class Cell:
    def __init__(self):
        """
        a stack of pieces.
        The stack will store pieces in the order they were placed on the cell.
        """
        self.pieces = []  # A stack of pieces

    def is_occupied(self):
        return len(self.pieces) > 0

    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self):
        if self.pieces:
            return self.pieces.pop()
        return None

    def get_top_piece(self):
        if self.pieces:
            return self.pieces[-1]
        return None

    def get_all_pieces(self):
        return self.pieces


class AvailablePieces:
    def __init__(self):
        self.g = 3  # Number of Grasshopper pieces
        self.a = 3  # Number of Ant pieces
        self.b = 2  # Number of Beetle pieces
        self.s = 2  # Number of Spider pieces
        self.q = 1  # Number of Queen Bee pieces

    def update_available_pieces(self, piece):
        if piece.get_name() == 'g':  # Grasshopper piece
            self.g -= 1
        elif piece.get_name() == 'a':  # Ant piece
            self.a -= 1
        elif piece.get_name() == 'b':  # Beetle piece
            self.b -= 1
        elif piece.get_name() == 's':  # Spider piece
            self.s -= 1
        elif piece.get_name() == 'q':  # Queen Bee piece
            self.q -= 1

    def is_this_piece_available(self, piece):
        """
        Checks if the piece selected to be played is available for the player or not.
        :param piece: The piece to check availability for (e.g., "g1", "a2", etc.)
        :return: True if the piece is available, False otherwise.
        """
        if piece.get_name().startswith('g'):  # Grasshopper piece
            return self.g > 0
        elif piece.get_name().startswith('a'):  # Ant piece
            return self.a > 0
        elif piece.get_name().startswith('b'):  # Beetle piece
            return self.b > 0
        elif piece.get_name().startswith('s'):  # Spider piece
            return self.s > 0
        elif piece.get_name().startswith('q'):  # Queen Bee piece
            return self.q > 0
        return False


class GameState:
    def __init__(self, player1Type, player2Type, player1Level, player2Level):
        self._initialize_state(player1Type, player2Type, player1Level, player2Level)


    def _initialize_state(self,player1Type, player2Type,player1Level,player2Level):
        self.state = [[Cell() for _ in range(50)] for _ in range(50)]  # Reset grid state
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
        self.playerWon = 0 # 1 if player 1 win and 2 if player 2 win


    def reset(self,player1Type, player2Type,player1Level,player2Level):
        self._initialize_state(player1Type,player2Type,player1Level,player2Level)


    def make_a_move(self):
        """
        Makes a move for the current player in case of a computer using the AI algorithms.
        should output 2 pairs (from_cell and to_cell)
        """
        pass


    def get_allowed_cells(self):
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
        cell = self.state[cell.r][cell.q]
        piece = cell.get_top_piece()
        if piece.get_name() == 'g':
            self.get_allowed_cells_for_grasshopper_from_cell(cell)
        elif piece.get_name() == 'a':
            self.get_allowed_cells_for_ant_from_cell(cell)
        elif piece.get_name() == 's':
            self.get_allowed_cells_for_spider_from_cell(cell)
        elif piece.get_name() == 'b':
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

        queen1Neighbors = self.q1.get_neighbors()
        queen2Neighbors = self.q2.get_neighbors()

        all_queen1_neighbors_occupied = all(
            self.state[neighbor.r][neighbor.q].is_occupied() for neighbor in queen1Neighbors)

        all_queen2_neighbors_occupied = all(
            self.state[neighbor.r][neighbor.q].is_occupied() for neighbor in queen2Neighbors)

        if all_queen1_neighbors_occupied:
            self.playerWon = 2
            return 2

        elif all_queen2_neighbors_occupied:
            self.playerWon = 1
            return 1

        return 0

    def update_state(self, piece:Piece, from_cell:CellPosition, to_cell:CellPosition):
        if from_cell != CellPosition(-1,-1):
            self.state[from_cell.q][from_cell.r].remove_piece()

        self.state[to_cell.q][to_cell.r].add_piece(piece)
        if piece.get_name()=='q':
            if piece.get_player() == 1:
                self.q1 = to_cell
            else:
                self.q2 = to_cell

        if self.turn == 1:
            self.turn = 2
            self.player1Moves+=1
            if from_cell == CellPosition(-1,-1):
                self.player1AvailablePieces.update_available_pieces(piece)
        else:
            self.turn = 1
            self.player2Moves+=1
            if from_cell == CellPosition(-1,-1):
                self.player2AvailablePieces.update_available_pieces(piece)






"""
 Pieces in the game:
 Grasshopper pieces >> g1, g2
 Ant pieces >> a1, a2
 Spider pieces >> s1, s2
 Beetle pieces >> b1, b2
 Queen pieces >> q1, q2
"""

