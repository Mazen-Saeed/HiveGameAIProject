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
        for move in moves:
            #print((2 - depth) * "  " + str(i) + " -->")
            #i += 1
            #print((2 - depth) * "  " + "Before clone: " + get_time_diff())
            #cloned_state = copy.deepcopy(game_state)
            #print((2 - depth) * "  " + "After clone: " + get_time_diff())
            
            #print("Before update state")
            #get_time_diff()
            #print("LEN OF PLACED PIECES before: ", len(cloned_state.players[cloned_state.turn].placed_pieces))
            #print((2 - depth) * "  " + "Before update state: " + get_time_diff())
            
            #print((2 - depth) * "  " + "BEFOR: ", game_state.current_allowed_placements, game_state.turn)
            #print((2 - depth) * "  " + "BEFOR: ", game_state.players[game_state.turn].unplaced_pieces, game_state.turn)
            game_state.update_state(game_state.state[move[1].r][move[1].q], move[2],
                                      game_state.state[move[0].r][move[0].q] if move[0] else None,
                                      True
                                      )
            evaluated_moves_list.append((self.evaluate(game_state, maximizing_player), move))
            game_state.undo_state(game_state.state[move[1].r][move[1].q], move[2],
                                  game_state.state[move[0].r][move[0].q] if move[0] else None)
            #print((2 - depth) * "  " + "AFTER: ", game_state.players[game_state.turn].unplaced_pieces, game_state.turn)
            #print((2 - depth) * "  " + "AFTER: ", game_state.current_allowed_placements, game_state.turn)
            #print((2 - depth) * "  " + "After update state: " + get_time_diff())
            
            #print("After update state")
            #get_time_diff()
            #print("LEN OF PLACED PIECES after: ", len(cloned_state.players[1 - cloned_state.turn].placed_pieces))
            ##print("PLACEMENT?", move[0], " MOVE? ", move[0], move[1])
            #print("CLONED STATE ID: ", cloned_state)
            #print("current player: ", 1 - cloned_state.turn)
        
        #print((2 - depth) * "  " + "Time after getting all moves evals: " + get_time_diff())
          
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            evaluated_moves_list.sort(key=lambda move: -move[0])
            for score, move in evaluated_moves_list:
                print((2 - depth) * "  " + f"({score}, {move})")
            for _, move in evaluated_moves_list:
                #print((2 - depth) * "  " + "BEFOR: ", game_state.players[game_state.turn].unplaced_pieces, game_state.turn)
                game_state.update_state(game_state.state[move[1].r][move[1].q], move[2],
                                        game_state.state[move[0].r][move[0].q] if move[0] else None,
                                        True
                                        )
                eval = self.alpha_beta(game_state, depth - 1, alpha, beta, False)
                game_state.undo_state(game_state.state[move[1].r][move[1].q], move[2],
                                  game_state.state[move[0].r][move[0].q] if move[0] else None)
                #print((2 - depth) * "  " + "AFTER: ", game_state.players[game_state.turn].unplaced_pieces, game_state.turn)
            
                #print((2 - depth) * "  " + "After  recursive call: " + get_time_diff())
                #get_time_diff()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    print(f"{alpha}/{beta}:________________________ PRUNED _____________________")
                    break
            #print("Exit alpha-beta")
            #get_time_diff()
            if depth == self.depth:
                print("############################################# BEST MOVE: ", best_move)
            return best_move if depth == self.depth else max_eval
        else:
            min_eval = float('inf')
            best_move = None
            evaluated_moves_list.sort(key=lambda move: move[0])
            
            for score, move in evaluated_moves_list:
                print((2 - depth) * "  " + f"({score}, {move})")
                
            for _, move in evaluated_moves_list:
                #print((2 - depth) * "  " + "BEFOR: ", game_state.players[game_state.turn].unplaced_pieces, game_state.turn)
                game_state.update_state(game_state.state[move[1].r][move[1].q], move[2],
                                      game_state.state[move[0].r][move[0].q] if move[0] else None,
                                      True
                                      )
                eval = self.alpha_beta(game_state, depth - 1, alpha, beta, True)
                game_state.undo_state(game_state.state[move[1].r][move[1].q], move[2],
                                  game_state.state[move[0].r][move[0].q] if move[0] else None)
                #print((2 - depth) * "  " + "AFTER: ", game_state.players[game_state.turn].unplaced_pieces, game_state.turn)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    print(f"{alpha}/{beta}:________________________ PRUNED _____________________")
                    break
            return best_move if depth == self.depth else min_eval