import copy

import time
previous_time = time.time()

def get_time_diff():
    global previous_time
    # Simulate work with different delays
    current_time = time.time()
    time_difference = current_time - previous_time
    res = f"{time_difference:.3f} seconds"
    previous_time = current_time
    return res 
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
        
        score = (len(player.placed_pieces) - len(opponent.placed_pieces)) * 10000
        #print("SCORE DIFF: ", score)
        if player.get_queen() and game_state.is_the_queen_surrounded(player.get_queen()):
            score -= 1000000000
        if opponent.get_queen() and game_state.is_the_queen_surrounded(opponent.get_queen()):
            score += 1000000000

        if player.get_queen() and opponent.get_queen():
            score += ((len(opponent.get_queen().get_occupied_neighbors(game_state.state)) -
                      len(player.get_queen().get_occupied_neighbors(game_state.state))) * 500)
                      
        #print("SCORE: ", score * factor)
        return score * factor

        # Example heuristic: number of placed pieces and queen safety

    def min_max(self, game_state, depth, maximizing_player):
        if depth == 0 or game_state.check_for_a_winner() != -1:
            return self.evaluate(game_state, 1 - maximizing_player)

        moves = game_state.getAllMovesForAI()

        if not moves:
            # No valid moves; return a default evaluation score
            return self.evaluate(game_state)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in moves:
                #cloned_state = copy.deepcopy(game_state)
                #cloned_state.update_state(cloned_state.state[move[1].r][move[1].q], move[2],
                #                          cloned_state.state[move[0].r][move[0].q] if move[0] else None
                #                          )
                game_state.update_state(game_state.state[move[1].r][move[1].q], move[2],
                                        game_state.state[move[0].r][move[0].q] if move[0] else None,
                                        True
                                        )
                eval = self.alpha_beta(game_state, depth - 1, alpha, beta, False)
                game_state.undo_state(game_state.state[move[1].r][move[1].q], move[2],
                                  game_state.state[move[0].r][move[0].q] if move[0] else None)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move if depth == self.depth else max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in moves:
                #cloned_state = copy.deepcopy(game_state)
                #cloned_state.update_state(cloned_state.state[move[1].r][move[1].q], move[2],
                #                          cloned_state.state[move[0].r][move[0].q] if move[0] else None
                #                          )
                game_state.update_state(game_state.state[move[1].r][move[1].q], move[2],
                                        game_state.state[move[0].r][move[0].q] if move[0] else None,
                                        True
                                        )
                eval = self.alpha_beta(game_state, depth - 1, alpha, beta, True)
                game_state.undo_state(game_state.state[move[1].r][move[1].q], move[2],
                                  game_state.state[move[0].r][move[0].q] if move[0] else None)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move if depth == self.depth else min_eval

    def alpha_beta(self, game_state, depth, alpha, beta, maximizing_player):
        #print("Entered alpha-beta:")
        #get_time_diff()
        #print((2 - depth) * "  " + f"Current player: {game_state.turn} and maximizing? {maximizing_player}")#, time on entry: " + get_time_diff())
        if depth == 0 or game_state.check_for_a_winner() != -1:
            return self.evaluate(game_state, 1 - maximizing_player)
        #print("Before getting moves: ")
        #get_time_diff()
        moves = game_state.getAllMovesForAI()
        #print("After getting moves: ")
        #get_time_diff()
        print((2 - depth) * "  " + f"CURRENT PLAYER: {game_state.turn}, maximizing? {maximizing_player}, NUMBER OF MOVES: {len(moves)}")
        if not moves:
            # No valid moves; return a default evaluation score
            return self.evaluate(game_state, 1 - maximizing_player)
        
        #print("MOVES LIST: ", moves)
        #print("PLAYER AVAILABLE PIECES: ", game_state.players[game_state.turn].unplaced_pieces)
        evaluated_moves_list = []
        #print((2 - depth) * "  " + "Time before getting all moves evals: " + get_time_diff())
        #i = 0
