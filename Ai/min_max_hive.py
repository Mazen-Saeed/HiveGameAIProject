import copy


class MinMaxAI:
    def __init__(self, depth=3):
        self.depth = depth


    def evaluate(self, game_state, maximizing_player):
        """
        Heuristic evaluation of the game state.
        """
        # The turns are flipped because we evaluate AFTER updating state
        player = game_state.players[1 - game_state.turn]
        opponent = game_state.players[game_state.turn]
        
        factor = 1 if maximizing_player else -1
        
        score = (len(player.placed_pieces) * 2 - len(opponent.placed_pieces)) * 1000
        #print("SCORE DIFF: ", score)
        if player.get_queen() and game_state.is_the_queen_surrounded(player.get_queen()):
            score -= 1000000000
        if opponent.get_queen() and game_state.is_the_queen_surrounded(opponent.get_queen()):
            score += 1000000000

        if player.get_queen() and opponent.get_queen():
            score += ((len(opponent.get_queen().get_occupied_neighbors(game_state.state)) -
                      len(player.get_queen().get_occupied_neighbors(game_state.state)) * 5) * 100)
                      
        #print("SCORE: ", score * factor)
        return score * factor

        # Example heuristic: number of placed pieces and queen safety

    def min_max(self, game_state, depth, maximizing_player):
        if depth == 0 or game_state.check_for_a_winner() != -1:
            return self.evaluate(game_state, maximizing_player)

        moves = game_state.getAllMovesForAI()

        if not moves:
            # No valid moves; return a default evaluation score
            return self.evaluate(game_state, maximizing_player)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in moves:
                cloned_state = copy.deepcopy(game_state)
                cloned_state.update_state(cloned_state.state[move[1].r][move[1].q], move[2],
                                          cloned_state.state[move[0].r][move[0].q] if move[0] else None
                                          )
                eval = self.min_max(cloned_state, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move if depth == self.depth else max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in moves:
                cloned_state = copy.deepcopy(game_state)
                cloned_state.update_state(cloned_state.state[move[1].r][move[1].q], move[2],
                                          cloned_state.state[move[0].r][move[0].q] if move[0] else None
                                          )
                eval = self.min_max(cloned_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move if depth == self.depth else min_eval

    def alpha_beta(self, game_state, depth, alpha, beta, maximizing_player):
        if depth == 0 or game_state.check_for_a_winner() != -1:
            return self.evaluate(game_state, 1 - maximizing_player)

        moves = game_state.getAllMovesForAI()
        if not moves:
            # No valid moves; return a default evaluation score
            return self.evaluate(game_state, maximizing_player)
        
        print("MOVES LIST: ", moves)
        print("PLAYER AVAILABLE PIECES: ", game_state.players[game_state.turn].unplaced_pieces)
        states_list = []
        for move in moves:
            cloned_state = copy.deepcopy(game_state)
            print("LEN OF PLACED PIECES before: ", len(cloned_state.players[cloned_state.turn].placed_pieces))
            cloned_state.update_state(cloned_state.state[move[1].r][move[1].q], move[2],
                                      cloned_state.state[move[0].r][move[0].q] if move[0] else None,
                                      True
                                      )
                                      
            print("LEN OF PLACED PIECES after: ", len(cloned_state.players[1 - cloned_state.turn].placed_pieces))
            print("PLACEMENT?", move[0], " MOVE? ", move[0], move[1])
            print("CLONED STATE ID: ", cloned_state)
            print("current player: ", 1 - cloned_state.turn)
            states_list.append((cloned_state, move))
           
          
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            states_list.sort(key=lambda cloned_state: -self.evaluate(cloned_state[0], maximizing_player))
            for state, move in states_list:
                print(self.evaluate(state, maximizing_player), move)
            for cloned_state, move in states_list:
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
            states_list.sort(key=lambda cloned_state: self.evaluate(cloned_state[0], maximizing_player))
            for cloned_state, move in states_list:
                eval = self.alpha_beta(cloned_state, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move if depth == self.depth else min_eval