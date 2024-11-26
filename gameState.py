class CellPosition:
    dr_odd = [-1, -1, 0, 1, 1, 0]
    dq_odd = [0, 1, 1, 1, 0, -1]
    dr_even = [-1, -1, 0,1,1,1]
    dq_even = [-1, 0, 1,0,-1,-1]


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

    def __hash__(self):
        return hash((self.q, self.r))  # Hash based on the tuple (q, r)

    def __str__(self):
        """
        Custom string representation for CellPosition.
        """
        return f"({self.q}, {self.r})"

    def get_neighbors(self):
        """
        Returns the neighboring CellPosition objects for the current position.
        """
        neighbors = []
        for i in range(len(CellPosition.dq_odd)):
            if self.r % 2 == 1:# Loop over the direction offsets
                new_q = self.q + CellPosition.dq_odd[i]
                new_r = self.r + CellPosition.dr_odd[i]
            else:
                new_q = self.q + CellPosition.dq_even[i]
                new_r = self.r + CellPosition.dr_even[i]

            if 0 <= new_q < 50 and 0 <= new_r < 50:
                neighbors.append(CellPosition(new_q, new_r))

        return neighbors


class Piece:
    """
     Pieces in the game:
     Grasshopper pieces >> g1, g2
     Ant pieces >> a1, a2
     Spider pieces >> s1, s2
     Beetle pieces >> b1, b2
     Queen pieces >> q1, q2
    """

    def __init__(self, name, player):
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
        else: # Queen Bee piece
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

    def _initialize_state(self, player1Type, player2Type, player1Level, player2Level):
        self.state = [[Cell() for _ in range(50)] for _ in range(50)]  # Reset grid state
        self.q1 = CellPosition(-1, -1)  # Reset player 1's queen bee position
        self.q2 = CellPosition(-1, -1)  # Reset player 2's queen bee position
        self.turn = 1  # Reset turn to player 1
        self.player1Moves = 0  # Reset player 1's move count
        self.player2Moves = 0  # Reset player 2's move count
        self.player1Type = player1Type  # "p" if player 1 is a person, "c" if a computer
        self.player2Type = player2Type  # "p" if player 2 is a person, "c" if a computer
        self.player1Level = player1Level  # "e" for easy, "m" for medium, "h" for hard, "p" if player
        self.player2Level = player2Level  # "e" for easy, "m" for medium, "h" for hard, "p" if player
        self.player1AvailablePieces = AvailablePieces()
        self.player2AvailablePieces = AvailablePieces()
        self.current_allowed_moves = set()
        self.playerWon = 0  # 1 if player 1 win and 2 if player 2 win

    def reset(self, player1Type, player2Type, player1Level, player2Level):
        self._initialize_state(player1Type, player2Type, player1Level, player2Level)

    def make_a_move(self):
        """
        Makes a move for the current player in case of a computer using the AI algorithms.
        should output 2 pairs (from_cell and to_cell)
        """
        pass


    def all_neighbours_from_player_or_empty(self, neighbours):
        """
        Checks if all neighbors of a given cell either belong to the specified player
        or are empty (not occupied by any piece).
        :param neighbours: List of CellPosition objects representing neighboring cells
        :param player_num: The player number to check for (1 or 2)
        :return: True if all neighbors belong to the player or are empty, False otherwise
        """
        at_least_one_neighbour = False
        for neighbour in neighbours:
            cell_obj = self.state[neighbour.r][neighbour.q]
            if cell_obj.is_occupied():
                top_piece = cell_obj.get_top_piece()
                at_least_one_neighbour = True
                if top_piece.get_player() != self.turn:
                    return False

        return at_least_one_neighbour

    def get_allowed_cells(self):
        """
        Retrieves allowed cells for placing a piece.
        """
        self.current_allowed_moves = set()
        if self.turn == 1:
            if self.player1Moves == 0:
                self.current_allowed_moves.add(CellPosition(25, 25))
        else:
            if self.player2Moves == 0:
                neighbors = CellPosition(25, 25).get_neighbors()
                for neighbor in neighbors:
                    self.current_allowed_moves.add(neighbor)

        if len(self.current_allowed_moves)>0:
            return self.current_allowed_moves

        for row in range(50):
            for col in range(50):
                cell = self.state[row][col]
                if not cell.is_occupied() and self.all_neighbours_from_player_or_empty(CellPosition(row,col).get_neighbors()):
                    self.current_allowed_moves.add(CellPosition(row,col))

        return self.current_allowed_moves

    def must_place_queen_bee(self):
        """
        Checks whether the current player must place their Queen Bee piece.

        :return:
            - True if the current player has made exactly 3 moves and their Queen Bee is still unplaced (position is (-1, -1)).
            - False if the Queen Bee has already been placed, or the player hasn't reached the required number of moves.
        """
        moves = self.player1Moves
        queen_bee_cell = self.q1

        if self.turn == 2:
            moves = self.player2Moves
            queen_bee_cell = self.q2

        if moves == 3 and queen_bee_cell == CellPosition(-1, -1):
            return True

        return False

    def can_move_pieces(self):
        """
        Determines whether the current player can move pieces on the board.
        return:
        - True if the current player's Queen Bee has been placed on the board (i.e., its position is not (-1, -1)).
        - False if the current player's Queen Bee has not been placed yet (i.e., its position is still (-1, -1)).
        """
        if self.turn==1:
            return self.q1 != CellPosition(-1,-1)
        else:
            return self.q2 != CellPosition(-1,-1)

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

        return self.current_allowed_moves

    def get_allowed_cells_for_grasshopper_from_cell(self, cell):
        pass

    def get_allowed_cells_for_ant_from_cell(self, cell):
        pass

    def get_allowed_cells_for_spider_from_cell(self, cell):
        pass

    def get_allowed_cells_for_beetle_from_cell(self, cell):
        pass

    def get_allowed_cells_for_queen_bee_from_cell(self, cell):
        pass

    def is_the_piece_on_cell_ok(self, cell: CellPosition):
        """
        The cell should be occupied and the piece should belong to the current player.
        :param cell: CellPosition representing the cell to check.
        :return: True if the cell is occupied by the current player's piece, False otherwise.
        """
        cell_obj = self.state[cell.r][cell.q]

        if not cell_obj.is_occupied():
            return False

        top_piece = cell_obj.get_top_piece()

        if top_piece.get_player() != self.turn:
            return False

        return True

    def is_this_cell_ok(self, cell: CellPosition):
        """
         Checks if the given cell is part of the allowed moves for the current player.
         :param cell: CellPosition representing the cell to check.
         :return: true if the cell is in the list of current allowed moves, False otherwise.
         """
        return cell in self.current_allowed_moves

    def check_for_a_winner(self):
        """
        Checks if either player's queen bee has all of its neighboring cells occupied,
        which is a winning condition in the game.

        :return:
        - 1 if player 1 wins (player 1's queen bee is surrounded),
        - 2 if player 2 wins (player 2's queen bee is surrounded),
        - 0 if no player has won yet (both queen bees are not surrounded).
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

    def update_state(self, piece: Piece, from_cell: CellPosition, to_cell: CellPosition):
        """
        Updates the game state after a move, including the position of the piece and any necessary changes
        to the turn, move count, and available pieces.

        :param piece: The piece being moved (e.g., a Queen Bee, Ant, Grasshopper, etc.)
        :param from_cell: The cell from which the piece is moving
        :param to_cell: The cell to which the piece is moving
        :return: None
        """
        if from_cell != CellPosition(-1, -1):
            self.state[from_cell.q][from_cell.r].remove_piece()

        self.state[to_cell.q][to_cell.r].add_piece(piece)
        if piece.get_name() == 'q':
            if piece.get_player() == 1:
                self.q1 = to_cell
            else:
                self.q2 = to_cell

        if self.turn == 1:
            self.turn = 2
            self.player1Moves += 1
            if from_cell == CellPosition(-1, -1):
                self.player1AvailablePieces.update_available_pieces(piece)
        else:
            self.turn = 1
            self.player2Moves += 1
            if from_cell == CellPosition(-1, -1):
                self.player2AvailablePieces.update_available_pieces(piece)


"""
To do:
 
  1) A draw may also be agreed if both players are in a position where they are 
     forced to move the same two pieces over and over again, without any possibility 
     of the stalemate being resolved.
 
  2) Unable to Move or to Place: If a player can nether place a new piece or move an
     existing piece, the turn passes to their opponent who then takes their turn again.
  
  3) make a move (AI algorithms)
  
  4) get_allowed_cells_given_the_piece_on_cell logic
  
  5) somthing is wrong with get_allowed_cells and maybe related to neighbours logic
  
"""
