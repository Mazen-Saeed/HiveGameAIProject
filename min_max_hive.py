import copy
import math
from gameState import GameState, CellPosition

class MinMaxAI:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def evaluate_game_state(self, game_state):
        """
        Evaluates the game state and assigns a heuristic score.
        :param game_state: The current game state.
        :return: A numerical score.
        """
        winner = game_state.check_for_a_winner()
        if winner == "p1":
            return math.inf  # Maximizing player wins
        elif winner == "p2":
            return -math.inf  # Minimizing player wins
        else:
            # Heuristic: Favor states with more moves for player 1 and fewer for player 2
            return len(game_state.get_allowed_cells()) if game_state.turn == 1 else -len(game_state.get_allowed_cells())

    def get_possible_moves(self, game_state):
        """
        Generate all possible moves for the current player.
        :param game_state: The current game state.
        :return: A list of (piece, from_cell, to_cell) tuples representing possible moves.
        """
        moves = []
        allowed_cells = game_state.get_allowed_cells()

        for from_cell in allowed_cells:
            piece = game_state.state[from_cell.r][from_cell.q]
            allowed_destinations = game_state.get_allowed_cells_given_the_piece_on_cell(from_cell)
            for to_cell in allowed_destinations:
                moves.append((piece, from_cell, to_cell))

        return moves

    def min_max(self, game_state, depth, is_maximizing):
        """
        Recursive implementation of the Min-Max algorithm.
        :param game_state: The current game state.
        :param depth: The current depth of the recursion.
        :param is_maximizing: Whether the current layer is maximizing or minimizing.
        :return: A tuple of (best_score, best_move).
        """
        if depth == 0 or game_state.check_for_a_winner() != "c":
            return self.evaluate_game_state(game_state), None

        best_score = -math.inf if is_maximizing else math.inf
        best_move = None

        for move in self.get_possible_moves(game_state):
            piece, from_cell, to_cell = move

            # Simulate the move
            new_game_state = copy.deepcopy(game_state)
            new_game_state.update_state(piece, from_cell, to_cell)

            # Recurse
            score, _ = self.min_max(new_game_state, depth - 1, not is_maximizing)

            if is_maximizing:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move

    def make_best_move(self, game_state):
        """
        Uses the Min-Max algorithm to make the best move for the current player.
        :param game_state: The current game state.
        :return: The chosen move.
        """
        _, best_move = self.min_max(game_state, self.max_depth, game_state.turn == 1)
        return best_move
