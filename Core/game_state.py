from pieces import Piece,Queen
from Ai import MinMaxAI,AlphaBetaPruningAI,AlphaBetaPruningWithIterativeDeepeningAI
from Core.cell_position import CellPosition
from Core.player import Player


class GameState:
    def __init__(self, player1Type="p", player2Type="p", player1Level="p", player2Level="p"):
        self._initialize_state(player1Type, player2Type, player1Level, player2Level)

    def reset(self, player1Type, player2Type, player1Level, player2Level):
        self._initialize_state(player1Type, player2Type, player1Level, player2Level)

    def _initialize_state(self, player1Type, player2Type, player1Level, player2Level):
        self.state = CellPosition.create_board() # Reset grid state
        # TODO: playerWon
        self.players = [Player(0, player1Type, player1Level), Player(1, player2Type, player2Level)]
        self.turn = 0  # Reset turn to player 1 (0 >> player 1 and 1 >> player 2)
        self.current_allowed_moves = {}
        self.current_allowed_placements = set()
        self.playerWon = -1  # 0 if player 1 win and 1 if player 2 win

    def make_a_move(self):
        """
        Makes a move for the current player in case of a computer using the AI algorithms.
        should output 2 pairs (from_cell and to_cell)
        """
        if self.players[self.turn].get_level() == "e":
            # use MinMaxAI
            pass
        elif self.players[self.turn].get_level() == "m":
            # use AlphaBetaPruningAI
            pass
        else:
            # use AlphaBetaPruningWithIterativeDeepeningAI
            pass

    def get_allowed_cells(self):
        """
        Retrieves allowed cells for placing a piece.
        """
        if self.current_allowed_placements:
            return self.current_allowed_placements

        if self.players[self.turn].get_moves_count() == 0:
            if self.turn == 0:
                self.current_allowed_placements.add(CellPosition.get_center_of_board(self.state))
            else:
                neighbors = CellPosition.get_center_of_board(self.state).get_neighbors(self.state)
                self.current_allowed_placements.update(neighbors)

        if self.current_allowed_placements:
            return self.current_allowed_placements

        self.current_allowed_placements =  Piece.get_available_placements(self.players[self.turn], self.state)

        return self.current_allowed_placements


    def must_place_queen_bee(self):
        """
        Checks whether the current player must place their Queen Bee piece.

        :return:
            - True if the current player has made exactly 3 moves and their Queen Bee is still unplaced (position is (-1, -1)).
            - False if the Queen Bee has already been placed, or the player hasn't reached the required number of moves.
        """
        if self.players[self.turn].get_moves_count() >= 3 and self.players[self.turn].queen_unplaced():
            return True
        return False

    def get_allowed_cells_given_the_piece_on_cell(self, cell: CellPosition):
        """
        Retrieves allowed moves for the specified cell.
        :param cell: An object of CellPosition representing the selected cell.
        ## NOTE: this should be the object from the game_board, because
                 otherwise it won't hold the pieces.
        """
        piece = cell.get_top_piece()

        if not self.current_allowed_moves:
            self.players[self.turn].is_there_allowed_moves_for_player(self.state,self.current_allowed_moves)

        return self.current_allowed_moves[piece]

    def is_the_piece_on_cell_ok(self, cell: CellPosition):
        """
        The cell should be occupied and the piece should belong to the current player.
        use it when a player tries to select a cell to move the piece in it
        :param cell: CellPosition representing the cell to check.
        :return: True if the cell is occupied by the current player's piece, False otherwise.
        """
        return cell.is_occupied() and cell.get_player_number() == self.turn

    def is_this_cell_ok(self, to_cell: CellPosition, piece:Piece=None, from_cell:CellPosition=None):
        """
        Checks if the given cell is part of the allowed moves for the current player.
        use it after a player chooses a piece to place or chooses a cell to move a piece to it.

        :param to_cell: The CellPosition the player is moving to/placing at
        :param piece: The piece the player is placing on the board, should be None if it's a move
        :param from_cell: CellPosition representing the cell the user will move to, None if it's a placement.
        :return: True if the cell is in the list of current allowed moves, False otherwise.
        """
        if piece:
            return to_cell in self.current_allowed_placements
        else:
            return (from_cell) and (from_cell in self.current_allowed_moves) and (to_cell in self.current_allowed_moves[from_cell])

    def is_the_piece_available(self,piece):
        """
        Checks if the piece selected to be played is available for the player or not.
        :param piece: The piece to check availability for (e.g., "Grasshopper(0)", "Ant(1)", etc.)
        :return: True if the piece is available, False otherwise.
        """
        return self.players[self.turn].unplaced_pieces.is_this_piece_available(piece)


    def player_allowed_to_move(self):
        return self.players[self.turn].get_queen() is not None


    def check_for_a_winner(self):
        """
        Checks if either player's queen has all of its neighboring cells occupied,
        which is a winning condition in the game.

        :return:
        - 0 if player 1 wins (player 1's queen bee is surrounded),
        - 1 if player 2 wins (player 2's queen bee is surrounded),
        - -1 if no player has won yet (both queen bees are not surrounded).
        """
        for player in self.players:
            queen = player.get_queen()  # Access the current player's queen
            if queen is None:
                continue  # If the player doesn't have their queen placed yet, skip to the next player

            queen_neighbors = queen.get_neighbors(self.state)  # Get the neighbors of the queen
            all_queen_neighbors_occupied = all(
                neighbor.is_occupied() for neighbor in queen_neighbors)  # Check if all neighbors are occupied

            if all_queen_neighbors_occupied:
                player_number = player.get_player_number()
                player_who_won = 1 - player_number
                self.playerWon = player_who_won
                return player_who_won # Return the winning player number (0 or 1)

        return -1  # No player has won yet

    def reset_for_new_turn(self):
        self.turn = 1 - self.turn
        self.current_allowed_moves = dict()
        self.current_allowed_placements = set()

    def update_state(self, to_cell: CellPosition, piece: Piece=None, from_cell: CellPosition=None):
        """
        Updates the game state after a move, including the position of the piece and any necessary changes
        to the turn, move count, and available pieces.

        :param to_cell: The cell to which the piece is placing/moving
        :param piece: The piece being placed (e.g., a Queen Bee, Ant, Grasshopper, etc.), None if player is moving a piece
        :param from_cell: The cell from which the piece is moving, None if the player is placing a piece
        :return: None
        """
        if from_cell:
            piece = from_cell.remove_piece()
        to_cell.add_piece(piece)

        if isinstance(piece, Queen):
            self.players[self.turn].set_queen(to_cell)

        self.players[self.turn].update_available_pieces(from_cell, to_cell)

        self.players[self.turn].moves_count += 1
        self.reset_for_new_turn()

    def player_allowed_to_play(self):
        """
        Computes every available placement and move for a player, and returns a boolean. True if
        the player can perform his turn (a placement or a move), False otherwise.

        :return: bool
        """
        self.current_allowed_placements = self.get_allowed_cells()
        # updates current allowed moves by reference
        self.players[self.turn].is_there_allowed_moves_for_player(self.state, self.current_allowed_moves)
        result = self.current_allowed_placements or self.current_allowed_moves
        if not result:
            self.reset_for_new_turn()
        return result
