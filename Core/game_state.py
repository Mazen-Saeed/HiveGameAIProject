from pieces import Piece,Grasshopper, Ant, Beetle, Spider, Queen
from Core.cell_position import CellPosition

class AvailablePieces:
    '''
    This class keeps track of all unplaced pieces.
    '''
    def __init__(self, player_number):
        self.pieces = [Grasshopper(player_number)] * 3
        self.pieces += [Ant(player_number)] * 3
        self.pieces += [Beetle(player_number)] * 2
        self.pieces += [Spider(player_number)] * 2
        self.pieces += [Queen(player_number)] * 1

    def __str__(self):
        return ", ".join(str(piece) for piece in self.pieces)

    def __repr__(self):
        return "[" + self.__str__() + "]"

    def __iter__(self):
        for piece in self.pieces:
            yield piece

    def update_available_pieces(self, piece):
        if piece in self.pieces:
            return self.pieces.pop(self.pieces.index(piece))
        else:
            raise ValueError(f"{piece} not found in available pieces: {[str(p) for p in self.pieces]}.")

    def is_this_piece_available(self, piece):
        """
        Checks if the piece selected to be played is available for the player or not.
        :param piece: The piece to check availability for (e.g., "g1", "a2", etc.)
        :return: True if the piece is available, False otherwise.
        """
        return piece in self.pieces


class GameState:
    def __init__(self, player1Type="p", player2Type="p", player1Level="p", player2Level="p"):
        self._initialize_state(player1Type, player2Type, player1Level, player2Level)

    def reset(self, player1Type, player2Type, player1Level, player2Level):
        self._initialize_state(player1Type, player2Type, player1Level, player2Level)

    def _initialize_state(self, player1Type, player2Type, player1Level, player2Level):
        self.state = CellPosition.create_board() # Reset grid state
        self.queens = [None, None]  # Reset player queen bee position
        self.turn = 0  # Reset turn to player 1
        self.player_moves = [0, 0]  # Reset players' move count
        self.player_types = [player1Type, player2Type]  # "p" if player is a person, "c" if a computer
        self.player_levels = [player1Level, player2Level]  # "e" for easy, "m" for medium, "h" for hard, "p" if player is a person
        self.player_available_pieces = [AvailablePieces(0), AvailablePieces(1)]
        self.current_allowed_moves = set()
        self.playerWon = 0  # 1 if player 1 win and 2 if player 2 win

    def make_a_move(self):
        """
        Makes a move for the current player in case of a computer using the AI algorithms.
        should output 2 pairs (from_cell and to_cell)
        """
        pass

    def get_allowed_cells(self):
        """
        Retrieves allowed cells for placing a piece.
        """
        self.current_allowed_moves = set()

        if self.player_moves[self.turn] == 0:
            if self.turn == 0:
                self.current_allowed_moves.add(CellPosition.get_center_of_board(self.state))
            else:
                neighbors = CellPosition.get_center_of_board(self.state).get_neighbors(self.state)
                self.current_allowed_moves.update(neighbors)

        if self.current_allowed_moves:
            return self.current_allowed_moves

        return Piece(self.turn).get_available_placements(self.state)


    def must_place_queen_bee(self):
        """
        Checks whether the current player must place their Queen Bee piece.

        :return:
            - True if the current player has made exactly 3 moves and their Queen Bee is still unplaced (position is (-1, -1)).
            - False if the Queen Bee has already been placed, or the player hasn't reached the required number of moves.
        """
        moves = self.player_moves[self.turn]
        if moves >= 3 and Queen(self.turn) in self.player_available_pieces[self.turn]:
            return True
        return False

    def get_allowed_cells_given_the_piece_on_cell(self, cell: CellPosition):
        """
        Retrieves allowed moves for the specified cell.
        :param cell: An object of CellPosition representing the selected cell
        ## NOTE: this should be the object from the game_board, because
                 otherwise it won't hold the pieces
        """
        piece = cell.get_top_piece()
        self.current_allowed_moves = piece.get_available_moves(cell, self.state)
        return self.current_allowed_moves

    def is_the_piece_on_cell_ok(self, cell: CellPosition):
        """
        The cell should be occupied and the piece should belong to the current player.
        :param cell: CellPosition representing the cell to check.
        :return: True if the cell is occupied by the current player's piece, False otherwise.
        """
        top_piece = cell.get_top_piece()
        return not cell.is_occupied() or top_piece.get_player() != self.turn

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
        for i, queen in enumerate(self.queens):
            if not queen:
                continue
            queen_neighbors = queen.get_neighbors(self.state)
            all_queen_neighbors_occupied = all(
                neighbor.is_occupied() for neighbor in queen_neighbors)
            if all_queen_neighbors_occupied:
                self.playerWon = i + 1
        return self.playerWon


    def update_state(self, piece: Piece, to_cell: CellPosition, from_cell: CellPosition = None):
        """
        Updates the game state after a move, including the position of the piece and any necessary changes
        to the turn, move count, and available pieces.

        :param piece: The piece being moved (e.g., a Queen Bee, Ant, Grasshopper, etc.)
        :param from_cell: The cell from which the piece is moving
        :param to_cell: The cell to which the piece is moving
        :return: None
        """
        if from_cell:
            piece = from_cell.remove_piece()
        to_cell.add_piece(piece)

        if isinstance(piece, Queen):
            self.queens[self.turn] = to_cell

        if not from_cell:
            self.player_available_pieces[self.turn].update_available_pieces(piece)

        self.player_moves[self.turn] += 1

        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0



    # Is there a point to this being here?
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
