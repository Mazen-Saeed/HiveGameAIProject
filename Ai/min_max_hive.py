class MinMaxAI:
    def __init__(self, depth=3):
        self.depth = depth

    def clone(self):
        import copy
        return copy.deepcopy(self)


    def evaluate(self, game_state):
        """
        Heuristic evaluation of the game state.
        """
        player = game_state.players[game_state.turn]
        opponent = game_state.players[1 - game_state.turn]

        # Example heuristic: number of placed pieces and queen safety
        score = len(player.placed_pieces) - len(opponent.placed_pieces)
        if player.get_queen() and game_state.is_the_queen_surrounded(player.get_queen()):
            score -= 100
        if opponent.get_queen() and game_state.is_the_queen_surrounded(opponent.get_queen()):
            score += 100

        return score


    def min_max(self, game_state, depth, maximizing_player):
        if depth == 0 or game_state.check_for_a_winner() != -1:
            return self.evaluate(game_state)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in game_state.getAllMovesForAI():
                cloned_state = game_state.clone()
                cloned_state.update_state(*move)
                eval = self.min_max(cloned_state, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move if depth == self.depth else max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in game_state.getAllMovesForAI():
                cloned_state = game_state.clone()
                cloned_state.update_state(*move)
                eval = self.min_max(cloned_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move if depth == self.depth else min_eval

    def alpha_beta(self, game_state, depth, alpha, beta, maximizing_player):
        if depth == 0 or game_state.check_for_a_winner() != -1:
            return self.evaluate(game_state)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_all_possible_moves(game_state):
                cloned_state = game_state.clone()
                cloned_state.update_state(*move)
                eval = self.alpha_beta(cloned_state, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move if depth == self.depth else max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_all_possible_moves(game_state):
                cloned_state = game_state.clone()
                cloned_state.update_state(*move)
                eval = self.alpha_beta(cloned_state, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move if depth == self.depth else min_eval
